import os
import sqlite3
import sys

# ANSI Colors for signature terminal blueprint aesthetic
GREEN = "\033[92m"
WHITE = "\033[97m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Constants derived from your payslip image
BASIC_SALARY = 2244750.0
FIXED_ALLOWANCE = 748250.0
HARI_KERJA_AKTIF = 24    # Calculated baseline for dynamic deduction (e.g., August 2026)

# Standard Overtime Rate Table mapped directly from your payslip image
STANDARD_RATES = {
    0.5: 12975,
    1.0: 25951,
    1.5: 43251,
    2.0: 60552,
    2.5: 77853,
    3.0: 95153,
    3.5: 112454,
    4.0: 129754,
    4.5: 147055,
    5.0: 164355,
    6.0: 198957,
    7.0: 121104,  # Derived base (242,208 / 2)
    8.0: 147500   # Base rate for 8 hours (295,000 / 2)
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_rp(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

def init_attendance_db():
    conn = sqlite3.connect('attendance_azkury.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            present TEXT NOT NULL,
            day TEXT NOT NULL,
            date INTEGER NOT NULL,
            month TEXT NOT NULL,
            year INTEGER NOT NULL,
            special_day TEXT NOT NULL,
            overtime REAL NOT NULL,
            overtime_salary REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def reindex_attendance_table():
    """Compresses IDs sequentially starting from 1 after rows are deleted or modified"""
    conn = sqlite3.connect('attendance_azkury.db')
    cursor = conn.cursor()
    cursor.execute("SELECT present, day, date, month, year, special_day, overtime, overtime_salary FROM attendance ORDER BY id ASC")
    rows = cursor.fetchall()
    
    cursor.execute("DELETE FROM attendance")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='attendance'")
    
    for row in rows:
        cursor.execute('''
            INSERT INTO attendance (present, day, date, month, year, special_day, overtime, overtime_salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', row)
    conn.commit()
    conn.close()

def check_duplicate_date(date, month, year):
    """Scans database to detect if attendance for the given date already exists"""
    conn = sqlite3.connect('attendance_azkury.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM attendance WHERE date=? AND month=? AND year=?", (date, month, year))
    record = cursor.fetchone()
    conn.close()
    return record is not None

def calculate_overtime_salary(hours, day_name, is_special):
    if hours == 0:
        return 0.0
    
    # Exact bypass for 8 hours weekend/special day to lock down Rp 295.000 flat
    if hours == 8.0 and (day_name.strip().lower() == 'sunday' or is_special.strip().lower() == 'y'):
        return 295000.0
        
    base_rate = STANDARD_RATES.get(hours, 0.0)
    # 2x multiplier rule for Sundays or Special Days (National Holidays)
    if day_name.strip().lower() == 'sunday' or is_special.strip().lower() == 'y':
        return base_rate * 2.0
    return base_rate

def display_banner():
    print(f"{GREEN}{BOLD}========================================={RESET}")
    print(f"{WHITE}{BOLD}            ATTENDANCE RECORD            {RESET}")
    print(f"{GREEN}{BOLD}========================================={RESET}")

def main_menu():
    while True:
        clear_screen()
        display_banner()
        print(f"{GREEN}1.{WHITE} ATTENDANCE")
        print(f"{GREEN}2.{WHITE} EDIT ATTENDANCE")
        print(f"{GREEN}3.{WHITE} DATABASE ATTENDANCE")
        print(f"{GREEN}4.{WHITE} DELETE ATTENDANCE")
        print(f"{GREEN}5.{WHITE} MONTHLY ATTENDANCE RECORD")
        print(f"{RED}[x]{WHITE} EXIT")
        print(f"{GREEN}========================================={RESET}")
        
        choice = input(f"{GREEN}Select option:{RESET} ").strip().lower()
        
        if choice == '1':
            menu_add_attendance()
        elif choice == '2':
            menu_edit_attendance_per_month()
        elif choice == '3':
            menu_display_database_per_month()
        elif choice == '4':
            menu_delete_attendance_per_month()
        elif choice == '5':
            menu_monthly_simulation_export()
        elif choice == 'x':
            print(f"\n{RED}Attendance subframe shut down. Execution terminated.{RESET}")
            sys.exit()
        else:
            input(f"\n{YELLOW}Invalid option. Press Enter to clear buffer...{RESET}")

def menu_add_attendance():
    clear_screen()
    print(f"{GREEN}{BOLD}[ MENU 1: LOG ATTENDANCE DATA ]{RESET}\n")
    
    while True:
        present_input = input(f"{WHITE}Attendance y/n/i/off: {RESET}").strip().lower()
        if present_input == 'y':
            present = "HADIR"
            break
        elif present_input == 'n':
            present = "ALFA"
            break
        elif present_input == 'i':
            present = "IZIN"
            break
        elif present_input == 'off':
            present = "OFF"
            break
        else:
            print(f"{RED}❌ Invalid option. Choose only y, n, i, or off.{RESET}")
        
    day = input(f"{WHITE}Day (e.g., Monday, Sunday): {RESET}").strip().capitalize()
    
    try:
        date = int(input(f"{WHITE}Date (1-31): {RESET}").strip())
        month = input(f"{WHITE}Month (e.g., May, June): {RESET}").strip().capitalize()
        year = int(input(f"{WHITE}Year (e.g., 2026): {RESET}").strip())
    except ValueError:
        print(f"\n{YELLOW}Invalid chronological format parameters.{RESET}")
        input()
        return
    
    if check_duplicate_date(date, month, year):
        print(f"\n{RED}{BOLD}[WARNING] Attendance data for this specific date ({date:02d}-{month}-{year}) already exists!{RESET}")
        print(f"{YELLOW}Operation aborted to prevent duplicate logs.{RESET}")
        input(f"\n{WHITE}Press Enter to return to Main Menu...{RESET}")
        return
        
    special_day = input(f"{WHITE}Special day / Red calendar date (y/n): {RESET}").strip().lower()
    
    try:
        overtime = float(input(f"{WHITE}Overtime hours (0 - 8): {RESET}").strip())
    except ValueError:
        overtime = 0.0

    if present == 'HADIR':
        salary = calculate_overtime_salary(overtime, day, special_day)
    else:
        overtime = 0.0
        salary = 0.0

    conn = sqlite3.connect('attendance_azkury.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO attendance (present, day, date, month, year, special_day, overtime, overtime_salary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (present, day, date, month, year, special_day.upper(), overtime, salary))
    conn.commit()
    conn.close()
    
    print(f"\n{GREEN}Attendance logged and encrypted successfully!{RESET}")
    input(f"\n{WHITE}Press Enter to return to Main Menu...{RESET}")

def select_database_period(cursor):
    """Reusable component to fetch and select available periods from database ordered chronologically"""
    cursor.execute("SELECT DISTINCT month, year FROM attendance")
    periods = cursor.fetchall()
    if not periods:
        return None
        
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    periods.sort(key=lambda x: (x[1], month_order.get(x[0], 0)))
        
    print(f"{WHITE}Available data periods discovered inside database:{RESET}")
    for idx, period in enumerate(periods, 1):
        print(f"  {GREEN}[{idx}]{WHITE} {period[0]} {period[1]}")
        
    try:
        selection = int(input(f"\n{GREEN}Select index number: {RESET}").strip())
        if 1 <= selection <= len(periods):
            return periods[selection - 1]
    except ValueError:
        pass
    return "INVALID"

def menu_edit_attendance_per_month():
    clear_screen()
    print(f"{GREEN}{BOLD}[ MENU 2: UPDATE ATTENDANCE CONFIGURATION BY MONTH ]{RESET}\n")
    
    conn = sqlite3.connect('attendance_azkury.db')
    cursor = conn.cursor()
    
    period = select_database_period(cursor)
    if not period:
        print(f"{YELLOW}No attendance archives generated yet.{RESET}")
        conn.close()
        input()
        return
    elif period == "INVALID":
        print(f"{YELLOW}Index selection outside bounds.{RESET}")
        conn.close()
        input()
        return
        
    selected_month, selected_year = period
    clear_screen()
    print(f"{GREEN}{BOLD}[ EDITING MATRIX FOR PERIOD: {selected_month.upper()} {selected_year} ]{RESET}\n")
    
    cursor.execute('''
        SELECT id, present, day, date, month, year, overtime, overtime_salary, special_day 
        FROM attendance 
        WHERE month=? AND year=? 
        ORDER BY date ASC
    ''', (selected_month, selected_year))
    rows = cursor.fetchall()
    
    if not rows:
        print(f"{YELLOW}No logs found for this selected month.{RESET}")
        conn.close()
        input()
        return
        
    local_id_map = {}
    for idx, r in enumerate(rows, 1):
        local_id_map[idx] = r[0]
        
        status_raw = str(r[1]).strip().upper()
        day_name = str(r[2]).strip().lower()
        is_spc = str(r[8]).strip().upper()
        
        is_sunday_or_special = (day_name == 'sunday' or is_spc == 'Y')
        
        # Row layout processing engine based on user requirements
        if status_raw == "HADIR" or status_raw == "PRESENT":
            if is_sunday_or_special:
                # Full line green
                print(f"{GREEN}  ID: {idx} | Status: [ HADIR ] | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Payout: {format_rp(r[7])}{RESET}")
            else:
                # Status green, sisa baris putih normal
                print(f"  {WHITE}ID: {idx} | Status: {GREEN}[ HADIR ]{WHITE} | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Payout: {format_rp(r[7])}{RESET}")
        elif status_raw == "ALFA":
            print(f"  {WHITE}ID: {idx} | Status: {RED}[ ALFA  ]{WHITE} | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Payout: {format_rp(r[7])}{RESET}")
        elif status_raw == "IZIN" or status_raw == "IJIN":
            print(f"  {WHITE}ID: {idx} | Status: {YELLOW}[ IJIN  ]{WHITE} | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Payout: {format_rp(r[7])}{RESET}")
        elif status_raw == "OFF":
            # Full line white normal
            print(f"  {WHITE}ID: {idx} | Status: [  OFF  ] | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Payout: {format_rp(r[7])}{RESET}")
        else:
            print(f"  {WHITE}ID: {idx} | Status: [ {status_raw:<5} ] | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Payout: {format_rp(r[7])}{RESET}")
        
    try:
        local_choice = int(input(f"\n{GREEN}Select Local ID Number to modify (e.g., 1): {RESET}").strip())
    except ValueError:
        print(f"{YELLOW}Parsing fault. Invalid format.{RESET}")
        conn.close()
        input()
        return
        
    if local_choice in local_id_map:
        target_id = local_id_map[local_choice]
        
        print(f"\n{YELLOW}Re-entering records for targeted Local ID {local_choice} {selected_month}:{RESET}\n")
        
        while True:
            edit_input = input(f"{WHITE}Attendance y/n/i/off: {RESET}").strip().lower()
            if edit_input == 'y':
                present = "HADIR"
                break
            elif edit_input == 'n':
                present = "ALFA"
                break
            elif edit_input == 'i':
                present = "IZIN"
                break
            elif edit_input == 'off':
                present = "OFF"
                break
            else:
                print(f"{RED}❌ Invalid option. Choose only y, n, i, or off.{RESET}")
                
        day = input(f"{WHITE}Day: {RESET}").strip().capitalize()
        date = int(input(f"{WHITE}Date: {RESET}").strip())
        month = input(f"{WHITE}Month: {RESET}").strip().capitalize()
        year = int(input(f"{WHITE}Year: {RESET}").strip())
        special_day = input(f"{WHITE}Special day / Red date (y/n): {RESET}").strip().lower()
        overtime = float(input(f"{WHITE}Overtime hours: {RESET}").strip())
        
        if present == 'HADIR':
            salary = calculate_overtime_salary(overtime, day, special_day)
        else:
            overtime = 0.0
            salary = 0.0
            
        cursor.execute('''
            UPDATE attendance 
            SET present=?, day=?, date=?, month=?, year=?, special_day=?, overtime=?, overtime_salary=?
            WHERE id=?
        ''', (present, day, date, month, year, special_day.upper(), overtime, salary, target_id))
        conn.commit()
        conn.close()
        
        reindex_attendance_table()
        print(f"\n{GREEN}Database row modified securely.{RESET}")
    else:
        print(f"\n{RED}Error: Local ID choice does not exist in this display buffer!{RESET}")
        conn.close()
    input(f"\n{WHITE}Press Enter to return...{RESET}")

def generate_report_logic(rows):
    total_standard_ot_salary = 0.0
    total_weekend_special_ot_salary = 0.0
    frequency_map = {k: 0 for k in STANDARD_RATES.keys()}
    
    weekend_special_7hr_count = 0
    holiday_special_7hr_count = 0
    weekend_special_8hr_count = 0
    holiday_special_8hr_count = 0
    
    hadir_count = 0
    alfa_count = 0
    izin_count = 0
    off_count = 0
    
    screen_lines = []
    clean_text_lines = []
    freq_lines = []
    clean_freq_lines = []
    
    for current_idx, r in enumerate(rows, start=1):
        row_id, present_raw, day, date, month, year, special_day, overtime, salary = r
        present = str(present_raw).strip().upper()
        day_name = str(day).strip().lower()
        is_spc = str(special_day).strip().upper()
        
        is_sunday_or_special = (day_name == 'sunday' or is_spc == 'Y')
        
        # Color and layout formatting matrix based on customized styling guidelines
        if present == 'HADIR' or present == 'PRESENT':
            hadir_count += 1
            display_status = "HADIR"
            if is_sunday_or_special:
                # Full line green
                screen_lines.append(f"{GREEN}  No: {current_idx:<2} ──► [ HADIR ] | {day:<9} {date:02d}-{month[:3]}-{year} | OT Hours: {overtime:<3} hrs | Salary: {format_rp(salary)}{RESET}")
            else:
                # Badge green, rest normal white
                screen_lines.append(f"  {WHITE}No: {current_idx:<2} ──► {GREEN}[ HADIR ]{WHITE} | {day:<9} {date:02d}-{month[:3]}-{year} | OT Hours: {overtime:<3} hrs | Salary: {format_rp(salary)}{RESET}")
        elif present == 'ALFA':
            alfa_count += 1
            display_status = "ALFA"
            screen_lines.append(f"  {WHITE}No: {current_idx:<2} ──► {RED}[ ALFA  ]{WHITE} | {day:<9} {date:02d}-{month[:3]}-{year} | OT Hours: {overtime:<3} hrs | Salary: {format_rp(salary)}{RESET}")
        elif present == 'IZIN' or present == 'IJIN':
            izin_count += 1
            display_status = "IJIN"
            screen_lines.append(f"  {WHITE}No: {current_idx:<2} ──► {YELLOW}[ IJIN  ]{WHITE} | {day:<9} {date:02d}-{month[:3]}-{year} | OT Hours: {overtime:<3} hrs | Salary: {format_rp(salary)}{RESET}")
        elif present == 'OFF':
            off_count += 1
            display_status = "OFF"
            # Full line white normal
            screen_lines.append(f"  {WHITE}No: {current_idx:<2} ──► [  OFF  ] | {day:<9} {date:02d}-{month[:3]}-{year} | OT Hours: {overtime:<3} hrs | Salary: {format_rp(salary)}{RESET}")
        else:
            display_status = present
            screen_lines.append(f"  {WHITE}No: {current_idx:<2} ──► [ {present:<5} ] | {day:<9} {date:02d}-{month[:3]}-{year} | OT Hours: {overtime:<3} hrs | Salary: {format_rp(salary)}{RESET}")
            
        clean_text_lines.append(f"  No: {current_idx:<2} --> [ {display_status:<5} ] | {day:<9} {date:02d}-{month[:3]}-{year} | OT Hours: {overtime:<3} hrs | Salary: {format_rp(salary)}")
        
        if (present == 'HADIR' or present == 'PRESENT') and overtime > 0:
            if is_sunday_or_special:
                total_weekend_special_ot_salary += salary
                if overtime == 7.0:
                    if day_name == 'sunday':
                        weekend_special_7hr_count += 1
                    else:
                        holiday_special_7hr_count += 1
                elif overtime == 8.0:
                    if day_name == 'sunday':
                        weekend_special_8hr_count += 1
                    else:
                        holiday_special_8hr_count += 1
            else:
                total_standard_ot_salary += salary
                if overtime in frequency_map:
                    frequency_map[overtime] += 1
                    
    freq_lines.append(f"  • Attendance Status Counter   : {GREEN}{hadir_count}x HADIR{RESET} | {WHITE}{off_count}x OFF{RESET} | {YELLOW}{izin_count}x IJIN{RESET} | {RED}{alfa_count}x ALFA{RESET}")
    freq_lines.append(f"  -------------------------------------------------------------------------------------------")
    clean_freq_lines.append(f"  • Attendance Status Counter   : {hadir_count}x HADIR | {off_count}x OFF | {izin_count}x IJIN | {alfa_count}x ALFA")
    clean_freq_lines.append(f"  -------------------------------------------------------------------------------------------")
    
    for hr in sorted(frequency_map.keys()):
        if hr in [7.0, 8.0]:
            continue
        count = frequency_map[hr]
        single_rate = STANDARD_RATES[hr]
        base_val = single_rate * count
        
        if count > 0:
            freq_lines.append(f"  • Overtime {hr:<3} hours : {GREEN}{count:<2}x{RESET} salary: {format_rp(single_rate)}  salary allocation ──► {GREEN}{format_rp(base_val)}{RESET}")
        else:
            freq_lines.append(f"  • Overtime {hr:<3} hours : {count:<2}x salary: {format_rp(single_rate)}  salary allocation ──► {format_rp(base_val)}")
            
        clean_freq_lines.append(f"  • Overtime {hr:<3} hours : {count:<2}x salary: {format_rp(single_rate)}  salary allocation ──► {format_rp(base_val)}")
        
    sun_7hr_rate = 242208.0
    spc_7hr_rate = 242208.0
    sun_8hr_rate = 295000.0
    spc_8hr_rate = 295000.0

    sun_7hr_salary = sun_7hr_rate * weekend_special_7hr_count
    spc_7hr_salary = spc_7hr_rate * holiday_special_7hr_count
    sun_8hr_salary = sun_8hr_rate * weekend_special_8hr_count
    spc_8hr_salary = spc_8hr_rate * holiday_special_8hr_count
    
    freq_lines.append(f"  -------------------------------------------------------------------------------------------")
    clean_freq_lines.append(f"  -------------------------------------------------------------------------------------------")
    
    if weekend_special_7hr_count > 0:
        freq_lines.append(f"  • Overtime Weekend 7 hours     : {GREEN}{weekend_special_7hr_count:<2}x{RESET} salary: {format_rp(sun_7hr_rate)}  salary allocation ──► {GREEN}{format_rp(sun_7hr_salary)}{RESET}")
    else:
        freq_lines.append(f"  • Overtime Weekend 7 hours     : {weekend_special_7hr_count:<2}x salary: {format_rp(sun_7hr_rate)}  salary allocation ──► {format_rp(sun_7hr_salary)}")

    if holiday_special_7hr_count > 0:
        freq_lines.append(f"  • Overtime Special Day 7 hours : {GREEN}{holiday_special_7hr_count:<2}x{RESET} salary: {format_rp(spc_7hr_rate)}  salary allocation ──► {GREEN}{format_rp(spc_7hr_salary)}{RESET}")
    else:
        freq_lines.append(f"  • Overtime Special Day 7 hours : {holiday_special_7hr_count:<2}x salary: {format_rp(spc_7hr_rate)}  salary allocation ──► {format_rp(spc_7hr_salary)}")

    if weekend_special_8hr_count > 0:
        freq_lines.append(f"  • Overtime Weekend 8 hours     : {GREEN}{weekend_special_8hr_count:<2}x{RESET} salary: {format_rp(sun_8hr_rate)}  salary allocation ──► {GREEN}{format_rp(sun_8hr_salary)}{RESET}")
    else:
        freq_lines.append(f"  • Overtime Weekend 8 hours     : {weekend_special_8hr_count:<2}x salary: {format_rp(sun_8hr_rate)}  salary allocation ──► {format_rp(sun_8hr_salary)}")

    if holiday_special_8hr_count > 0:
        freq_lines.append(f"  • Overtime Special Day 8 hours : {GREEN}{holiday_special_8hr_count:<2}x{RESET} salary: {format_rp(spc_8hr_rate)}  salary allocation ──► {GREEN}{format_rp(spc_8hr_salary)}{RESET}")
    else:
        freq_lines.append(f"  • Overtime Special Day 8 hours : {holiday_special_8hr_count:<2}x salary: {format_rp(spc_8hr_rate)}  salary allocation ──► {format_rp(spc_8hr_salary)}")
    
    clean_freq_lines.append(f"  • Overtime Weekend 7 hours     : {weekend_special_7hr_count:<2}x salary: {format_rp(sun_7hr_rate)}  salary allocation ──► {format_rp(sun_7hr_salary)}")
    clean_freq_lines.append(f"  • Overtime Special Day 7 hours : {holiday_special_7hr_count:<2}x salary: {format_rp(spc_7hr_rate)}  salary allocation ──► {format_rp(spc_7hr_salary)}")
    clean_freq_lines.append(f"  • Overtime Weekend 8 hours     : {weekend_special_8hr_count:<2}x salary: {format_rp(sun_8hr_rate)}  salary allocation ──► {format_rp(sun_8hr_salary)}")
    clean_freq_lines.append(f"  • Overtime Special Day 8 hours : {holiday_special_8hr_count:<2}x salary: {format_rp(spc_8hr_rate)}  salary allocation ──► {format_rp(spc_8hr_salary)}")
    
    potongan_per_hari = (BASIC_SALARY + FIXED_ALLOWANCE) / HARI_KERJA_AKTIF
    alfa_deduction_total = alfa_count * potongan_per_hari
    izin_deduction_total = izin_count * potongan_per_hari
    combined_deduction = alfa_deduction_total + izin_deduction_total
    
    if alfa_count > 0:
        freq_lines.append(f"  • Total Alfa Deduction ({alfa_count:<2}x Mangkir Kerja) ──► {RED}-{format_rp(alfa_deduction_total)}{RESET}")
    else:
        freq_lines.append(f"  • Total Alfa Deduction ({alfa_count:<2}x Mangkir Kerja) ──► -{format_rp(alfa_deduction_total)}")
        
    if izin_count > 0:
        freq_lines.append(f"  • Total Ijin Deduction ({izin_count:<2}x Ijin Resmi)    ──► {YELLOW}-{format_rp(izin_deduction_total)}{RESET}")
    else:
        freq_lines.append(f"  • Total Ijin Deduction ({izin_count:<2}x Ijin Resmi)    ──► -{format_rp(izin_deduction_total)}")
        
    clean_freq_lines.append(f"  • Total Alfa Deduction ({alfa_count:<2}x Mangkir Kerja) ──► -{format_rp(alfa_deduction_total)}")
    clean_freq_lines.append(f"  • Total Ijin Deduction ({izin_count:<2}x Ijin Resmi)    ──► -{format_rp(izin_deduction_total)}")
    
    total_all_overtime = total_standard_ot_salary + total_weekend_special_ot_salary
    gross_payout_sum = BASIC_SALARY + FIXED_ALLOWANCE + total_all_overtime
    final_net_salary = gross_payout_sum - combined_deduction
    
    return (screen_lines, clean_text_lines, freq_lines, clean_freq_lines, 
            total_standard_ot_salary, total_weekend_special_ot_salary, 
            alfa_deduction_total, izin_deduction_total, final_net_salary)

def menu_display_database_per_month():
    clear_screen()
    print(f"{GREEN}{BOLD}[ MENU 3: DATABASE ATTENDANCE BY MONTH ]{RESET}\n")
    
    conn = sqlite3.connect('attendance_azkury.db')
    cursor = conn.cursor()
    
    period = select_database_period(cursor)
    if not period:
        print(f"{YELLOW}No data logs found inside the database.{RESET}")
        conn.close()
        input()
        return
    elif period == "INVALID":
        print(f"{YELLOW}Index selection outside bounds.{RESET}")
        conn.close()
        input()
        return
        
    selected_month, selected_year = period
    
    cursor.execute('''
        SELECT id, present, day, date, month, year, special_day, overtime, overtime_salary 
        FROM attendance 
        WHERE month=? AND year=? 
        ORDER BY date ASC
    ''', (selected_month, selected_year))
    monthly_rows = cursor.fetchall()
    conn.close()
    
    (screen_lines, _, freq_lines, _, ts_ot, tw_ot, 
     alfa_ded, izin_ded, net_salary) = generate_report_logic(monthly_rows)
    
    print(f"\n{GREEN}{BOLD}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f" {WHITE}{BOLD}DATABASE MATRIX TRACKER: {selected_month.upper()} {selected_year}{RESET}")
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    for line in screen_lines:
        print(line)
    print(f"{GREEN}{BOLD}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f" {WHITE}{BOLD}FREQUENCY & ATTENDANCE ANALYSIS (DETAILED PER MONTH){RESET}")
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    for line in freq_lines:
        print(line)
    print(f"{GREEN}{BOLD}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f" {WHITE}{BOLD}TOTAL INTEGRATED PAYROLL OUTCOME ARCHITECTURE{RESET}")
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f"  {WHITE}Basic Salary (Gaji Pokok)             : {GREEN}{format_rp(BASIC_SALARY)}{RESET}")
    print(f"  {WHITE}Fixed Allowance (Tunjangan Pokok)     : {GREEN}{format_rp(FIXED_ALLOWANCE)}{RESET}")
    print(f"  {WHITE}Standard Weekday Overtime              : {GREEN}{format_rp(ts_ot)}{RESET}")
    print(f"  {WHITE}Weekend & Special Overtime Payout     : {GREEN}{format_rp(tw_ot)}{RESET}")
    print(f"  {GREEN}                                        {BOLD}───────────────────────────────────────────{RESET}")
    print(f"  {WHITE}Total Deductions (Alfa + Izin)        : {RED:}-{format_rp(alfa_ded + izin_ded)}{RESET}")
    print(f"  {GREEN}                                        {BOLD}───────────────────────────────────────────{RESET}")
    print(f"  {CYAN}{BOLD}TOTAL NET SALARY PAYOUT RECEIVABLE    : {YELLOW}{format_rp(net_salary)}{RESET}")
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    
    input(f"\n{WHITE}End of structural attendance trace. Press Enter to return to Menu...{RESET}")

def menu_delete_attendance_per_month():
    clear_screen()
    print(f"{GREEN}{BOLD}[ MENU 4: WIPE ATTENDANCE LOG ELEMENT BY MONTH ]{RESET}\n")
    
    conn = sqlite3.connect('attendance_azkury.db')
    cursor = conn.cursor()
    
    period = select_database_period(cursor)
    if not period:
        print(f"{YELLOW}Database is blank or no logs found. Operation aborted.{RESET}")
        conn.close()
        input()
        return
    elif period == "INVALID":
        print(f"{YELLOW}Index selection outside bounds.{RESET}")
        conn.close()
        input()
        return
        
    selected_month, selected_year = period
    clear_screen()
    print(f"{GREEN}{BOLD}[ PURGING ARCHIVES FOR PERIOD: {selected_month.upper()} {selected_year} ]{RESET}\n")
    
    cursor.execute('''
        SELECT id, present, day, date, month, year, overtime, overtime_salary, special_day 
        FROM attendance 
        WHERE month=? AND year=? 
        ORDER BY date ASC
    ''', (selected_month, selected_year))
    rows = cursor.fetchall()
    
    if not rows:
        print(f"{YELLOW}No logs found for this selected month.{RESET}")
        conn.close()
        input()
        return
        
    local_id_map = {}
    for idx, r in enumerate(rows, 1):
        local_id_map[idx] = r[0]
        status_raw = str(r[1]).strip().upper()
        day_name = str(r[2]).strip().lower()
        is_spc = str(r[8]).strip().upper()
        
        is_sunday_or_special = (day_name == 'sunday' or is_spc == 'Y')
        
        if status_raw == "HADIR" or status_raw == "PRESENT":
            if is_sunday_or_special:
                print(f"{GREEN}  ID: {idx} | Status: [ HADIR ] | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Value: {format_rp(r[7])}{RESET}")
            else:
                print(f"  {WHITE}ID: {idx} | Status: {GREEN}[ HADIR ]{WHITE} | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Value: {format_rp(r[7])}{RESET}")
        elif status_raw == "ALFA":
            print(f"  {WHITE}ID: {idx} | Status: {RED}[ ALFA  ]{WHITE} | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Value: {format_rp(r[7])}{RESET}")
        elif status_raw == "IZIN" or status_raw == "IJIN":
            print(f"  {WHITE}ID: {idx} | Status: {YELLOW}[ IJIN  ]{WHITE} | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Value: {format_rp(r[7])}{RESET}")
        elif status_raw == "OFF":
            print(f"  {WHITE}ID: {idx} | Status: [  OFF  ] | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Value: {format_rp(r[7])}{RESET}")
        else:
            print(f"  {WHITE}ID: {idx} | Status: [ {status_raw:<5} ] | Date: {r[3]:02d}-{r[4][:3]}-{r[5]} ({r[2]}) | OT: {r[6]} hrs | Value: {format_rp(r[7])}{RESET}")
        
    try:
        local_choice = int(input(f"\n{RED}Enter Local ID Number to delete permanently (e.g., 1): {RESET}").strip())
    except ValueError:
        print(f"{YELLOW}Invalid parsing conversion matrix.{RESET}")
        conn.close()
        input()
        return
        
    if local_choice in local_id_map:
        target_id = local_id_map[local_choice]
        
        cursor.execute("DELETE FROM attendance WHERE id=?", (target_id,))
        conn.commit()
        conn.close()
        
        reindex_attendance_table()
        print(f"\n{GREEN}Record purged successfully. Database auto-reindexed perfectly!{RESET}")
    else:
        print(f"\n{RED}Error: Local ID choice does not exist in this display buffer! Purge aborted.{RESET}")
        conn.close()
    input(f"\n{WHITE}Press Enter to finalize...{RESET}")

def menu_monthly_simulation_export():
    clear_screen()
    print(f"{GREEN}{BOLD}[ MENU 5: MONTHLY ATTENDANCE RECORD ]{RESET}\n")
    
    conn = sqlite3.connect('attendance_azkury.db')
    cursor = conn.cursor()
    
    period = select_database_period(cursor)
    if not period:
        print(f"{YELLOW}No monthly chronological segments found inside database ledger.{RESET}")
        conn.close()
        input()
        return
    elif period == "INVALID":
        print(f"{YELLOW}Index selection outside bounds.{RESET}")
        conn.close()
        input()
        return
        
    selected_month, selected_year = period
    
    cursor.execute('''
        SELECT id, present, day, date, month, year, special_day, overtime, overtime_salary 
        FROM attendance 
        WHERE month=? AND year=? 
        ORDER BY date ASC
    ''', (selected_month, selected_year))
    monthly_rows = cursor.fetchall()
    conn.close()
    
    (screen_lines, clean_text_lines, freq_lines, clean_freq_lines, 
     ts_ot, tw_ot, alfa_ded, izin_ded, net_salary) = generate_report_logic(monthly_rows)
    
    print(f"\n{CYAN}{BOLD}>>> PREVIEW SIMULATION FOR {selected_month.upper()} {selected_year} <<<{RESET}")
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    for line in screen_lines:
        print(line)
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f" {WHITE}{BOLD}FREQUENCY & ATTENDANCE ANALYSIS{RESET}")
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    for line in freq_lines:
        print(line)
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f"  {WHITE}Basic Salary             : {format_rp(BASIC_SALARY)}{RESET}")
    print(f"  {WHITE}Fixed Allowance          : {format_rp(FIXED_ALLOWANCE)}{RESET}")
    print(f"  {WHITE}Accumulated Overtime     : {format_rp(ts_ot + tw_ot)}{RESET}")
    print(f"  {WHITE}Total Absen Deductions   : -{format_rp(alfa_ded + izin_ded)}{RESET}")
    print(f"  {CYAN}{BOLD}NET PAYOUT ESTIMATION    : {YELLOW}{format_rp(net_salary)}{RESET}")
    print(f"{GREEN}─────────────────────────────────────────────────────────────────────────────────────────────{RESET}")
    
    export_choice = input(f"\n{WHITE}Do you want to export this simulation to a .txt file? (y/n): {RESET}").strip().lower()
    if export_choice == 'y':
        filename = f"report_{selected_month}_{selected_year}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=============================================================================================\n")
                f.write(f"                  EXECUTIVE PAYROLL & ATTENDANCE REPORT - {selected_month.upper()} {selected_year}\n")
                f.write("=============================================================================================\n\n")
                f.write("[ PART 1: DAILY ATTENDANCE LOGS ]\n")
                f.write("---------------------------------------------------------------------------------------------\n")
                for line in clean_text_lines:
                    f.write(line + "\n")
                f.write("---------------------------------------------------------------------------------------------\n\n")
                f.write("[ PART 2: OVERTIME FREQUENCY BREAKDOWN & SUMMARY ]\n")
                f.write("---------------------------------------------------------------------------------------------\n")
                for line in clean_freq_lines:
                    clean_line = line.replace("──►", "-->")
                    f.write(clean_line + "\n")
                f.write("---------------------------------------------------------------------------------------------\n\n")
                f.write("[ PART 3: FINAL MONTHLY PAYROLL ARCHITECTURE ]\n")
                f.write("---------------------------------------------------------------------------------------------\n")
                f.write(f"  Basic Salary (Gaji Pokok)             : {format_rp(BASIC_SALARY)}\n")
                f.write(f"  Fixed Allowance (Tunjangan Pokok)     : {format_rp(FIXED_ALLOWANCE)}\n")
                f.write(f"  Standard Weekday Overtime             : {format_rp(ts_ot)}\n")
                f.write(f"  Weekend & Special Overtime Payout     : {format_rp(tw_ot)}\n")
                f.write(f"  Total Absen Deductions                : -{format_rp(alfa_ded + izin_ded)}\n")
                f.write("  -------------------------------------------------------------------------------------------\n")
                f.write(f"  TOTAL NET SALARY RECEIVABLE           : {format_rp(net_salary)}\n")
                f.write("=============================================================================================\n")
                f.write("STATUS: ARCHIVED AND SECURED.\n")
                
            print(f"\n{GREEN}{BOLD}[SUCCESS] File saved perfectly as '{filename}'!{RESET}")
        except Exception as e:
            print(f"\n{RED}[ERROR] Failed to write file to storage: {e}{RESET}")
            
    input(f"\n{WHITE}Press Enter to return to main menu...{RESET}")

if __name__ == "__main__":
    init_attendance_db()
    main_menu()
