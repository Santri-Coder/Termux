import os
import sys
import time
import json
import random
from datetime import datetime

# Warna ANSI untuk Termux
HIJAU = '\033[1;32m'
PUTIH = '\033[1;37m'
MERAH = '\033[1;31m'
KUNING = '\033[1;33m'
B_BIRU = '\033[1;34m'
NORMAL = '\033[0m'

class CatatanKeuangan:
    def __init__(self):
        self.file_db = os.path.expanduser("~/database_keuangan.json")
        self.data_master = self.load_data()
        if not isinstance(self.data_master, dict):
            self.data_master = {"transaksi": [], "hutang": []}

    def load_data(self):
        if os.path.exists(self.file_db):
            try:
                with open(self.file_db, 'r') as f:
                    return json.load(f)
            except:
                return {"transaksi": [], "hutang": []}
        return {"transaksi": [], "hutang": []}

    def save_data(self):
        msg_save = ["[*] Sinkronisasi Database...", "[*] Backup Data...", "[*] Mengunci Record..."]
        self.ketik(f"\n{B_BIRU}{random.choice(msg_save)}")
        try:
            with open(self.file_db, 'w') as f:
                json.dump(self.data_master, f, indent=4)
            time.sleep(0.5)
        except IOError as e:
            print(f"{MERAH}Gagal simpan: {e}{NORMAL}")

    def ketik(self, teks, speed=0.02):
        for char in teks:
            sys.stdout.write(char); sys.stdout.flush(); time.sleep(speed)
        print()

    def banner(self):
        os.system('clear')
        print(f"{HIJAU}▐▓█▀▀▀▀▀▀▀▀▀█▓▌  ▄▄▄▄▄\n▐▓█Robot🤖  █▓▌  █▄▄▄█\n▐▓█   Jarvis█▓▌  █▄▄▄█\n▐▓█▄▄▄▄▄▄▄▄▄█▓▌  █▄▄▄█\n    ▄▄███▄▄      █████")
        print(f"{PUTIH} ╔══════════════════════════════════════════╗\n ║{HIJAU}      Jarvis Financial Database v3.1      {PUTIH}║\n ╚══════════════════════════════════════════╝{NORMAL}")

    def validasi_tanggal(self, d, m, y):
        try: return datetime(year=int(y), month=int(m), day=int(d)).strftime("%d-%m-%Y")
        except: return None

    def filter_tampilkan(self):
        trx = self.data_master["transaksi"]
        lebar = 71
        print(f"{PUTIH}{'='*lebar}\n| {HIJAU}{'NO':<3} | {'TANGGAL':<10} | {'KETERANGAN':<12} | {'JENIS':<12} | {'NOMINAL':<18}{PUTIH} |\n{'-'*(lebar-2)}")
        if not trx:
            print(f"|{PUTIH}{'DATABASE KOSONG':^69}|")
        for i, item in enumerate(trx):
            warna = HIJAU if item['jenis'] == "Pemasukan" else MERAH
            ket = (item['ket'][:9] + '..') if len(item['ket']) > 12 else item['ket']
            print(f"| {PUTIH}{i+1:<3} | {item['tanggal']:<10} | {ket:<12} | {warna}{item['jenis']:<12}{PUTIH} | Rp {item['nominal']:,.0f} |")
        print(f"{'='*lebar}{NORMAL}")

    def filter_tampilkan_hutang(self):
        htg = self.data_master["hutang"]
        lebar = 71
        print(f"{PUTIH}{'='*lebar}\n| {HIJAU}{'NO':<3} | {'TANGGAL':<10} | {'PEMBERI':<12} | {'STATUS':<12} | {'SISA HUTANG':<18}{PUTIH} |\n{'-'*(lebar-2)}")
        if not htg:
            print(f"|{PUTIH}{'DATABASE KOSONG':^69}|")
        for i, item in enumerate(htg):
            warna = HIJAU if item['status'] == "LUNAS" else MERAH
            pemb = (item['pemberi'][:9] + '..') if len(item['pemberi']) > 12 else item['pemberi']
            print(f"| {PUTIH}{i+1:<3} | {item['tgl']:<10} | {pemb:<12} | {warna}{item['status']:<12}{PUTIH} | Rp {item['sisa']:,.0f} |")
        print(f"{'='*lebar}{NORMAL}")

    # --- MENU 1 & 2 ---
    def tambah_transaksi(self, jenis):
        self.banner()
        print(f"{PUTIH}--- Form {jenis} ---")
        try:
            nom = float(input(f"{HIJAU}>>{PUTIH} Nominal: "))
            t = input("   Tanggal: "); b = input("   Bulan: "); th = input("   Tahun: ")
            ket = input(f"{HIJAU}>>{PUTIH} Keterangan: ")
            tgl_v = self.validasi_tanggal(t, b, th)
            if tgl_v:
                self.data_master["transaksi"].append({"jenis": jenis, "nominal": nom, "tanggal": tgl_v, "ket": ket.lower()})
                self.save_data()
                self.ketik(f"{HIJAU}[SUCCESS] Data tersimpan.")
            else: print(f"{MERAH}Format Tanggal Salah!")
        except: print(f"{MERAH}Input Error!")
        input("\nEnter...")

    # --- MENU 3 ---
    def tampilkan_total(self):
        self.banner()
        self.filter_tampilkan()
        trx = self.data_master["transaksi"]
        masuk = sum(i['nominal'] for i in trx if i['jenis'] == "Pemasukan")
        keluar = sum(i['nominal'] for i in trx if i['jenis'] == "Pengeluaran")
        print(f"{HIJAU}Total Pemasukan   : Rp {masuk:,.0f}\n{MERAH}Total Pengeluaran : Rp {keluar:,.0f}\n{PUTIH}TOTAL SALDO BERSIH: Rp {masuk-keluar:,.0f}{NORMAL}")
        input("\nEnter...")

    # --- MENU 4 ---
    def menu_perbaikan(self):
        while True:
            self.banner()
            print(f"{PUTIH}--- Edit & Hapus Data Transaksi ---")
            print("1. Edit Data\n2. Hapus Data\n3. Kembali")
            p = input(f"\n{HIJAU}Azzkury-ID{PUTIH} > ")
            if p == "3": break
            self.filter_tampilkan()
            trx = self.data_master["transaksi"]
            if not trx: input("Database kosong!"); continue
            try:
                idx = int(input(f"{HIJAU}>>{PUTIH} Pilih Nomor Data: ")) - 1
                if 0 <= idx < len(trx):
                    if p == "1":
                        nom = float(input("Nominal Baru: "))
                        t = input("Tgl: "); b = input("Bln: "); th = input("Thn: ")
                        ket = input("Keterangan Baru: ")
                        tgl_v = self.validasi_tanggal(t, b, th)
                        if tgl_v:
                            trx[idx].update({"nominal": nom, "tanggal": tgl_v, "ket": ket.lower()})
                            self.save_data()
                    elif p == "2":
                        if input("Yakin hapus? (y/n): ") == "y": trx.pop(idx); self.save_data()
                else: print(f"{MERAH}Nomor tidak valid!{NORMAL}")
            except: print("Error!")
            input("\nEnter...")

    # --- MENU 6 ---
    def evaluasi(self):
        self.banner()
        trx = self.data_master["transaksi"]
        masuk = sum(i['nominal'] for i in trx if i['jenis'] == "Pemasukan")
        if masuk == 0: print(f"{MERAH}Pemasukan Rp 0, tidak bisa evaluasi."); input(); return
        primer = sum(i['nominal'] for i in trx if i['jenis'] == "Pengeluaran" and any(x in i['ket'] for x in ['makan','bensin','listrik','kos','hutang']))
        persen = (primer / masuk) * 100
        print(f"{PUTIH}Evaluasi Pengeluaran Primer: Rp {primer:,.0f} ({persen:.1f}%)\nStatus: {HIJAU if persen <= 70 else MERAH}{'Wajar' if persen <= 70 else 'Bahaya/Boros'}{NORMAL}")
        input("\nEnter...")

    # --- MENU 7 ---
    def catat_hutang(self):
        self.banner()
        try:
            nom = float(input(f"{HIJAU}>>{PUTIH} nominal hutang : "))
            t = input("   Tanggal        : "); b = input("   Bulan          : "); th = input("   Tahun          : ")
            pemb = input(f"{HIJAU}>>{PUTIH} pemberi hutang: ")
            tgl_v = self.validasi_tanggal(t, b, th)
            if tgl_v:
                self.data_master["hutang"].append({"pemberi": pemb, "nominal": nom, "sisa": nom, "tgl": tgl_v, "status": "BELUM LUNAS", "bayar": []})
                self.save_data()
        except: print("Error!")
        input("\nEnter...")

    # --- MENU 8 ---
    def pelunasan_hutang(self):
        self.banner()
        h_list = [h for h in self.data_master["hutang"] if h["status"] == "BELUM LUNAS"]
        if not h_list: print("Tidak ada hutang aktif."); input(); return
        for i, h in enumerate(h_list): print(f"{i+1}. {h['pemberi']} (Sisa: Rp {h['sisa']:,.0f})")
        try:
            p = int(input(f"\n{HIJAU}>>{PUTIH} Pilih nomor: ")) - 1
            nom_b = float(input("   Nominal pembayaran : "))
            t = input("   Tanggal            : "); b = input("   Bulan              : "); th = input("   Tahun              : ")
            pen = input("   Penerima           : ")
            h_list[p]["bayar"].append({"tgl": f"{t}-{b}-{th}", "nom": nom_b, "pen": pen})
            h_list[p]["sisa"] -= nom_b
            if h_list[p]["sisa"] <= 0: h_list[p]["sisa"] = 0; h_list[p]["status"] = "LUNAS"
            self.save_data()
        except: print("Gagal!")
        input("\nEnter...")

    # --- MENU 9 ---
    def data_hutang_lengkap(self):
        self.banner()
        print(f"{PUTIH}{'='*65}\n{'DATA HUTANG & PELUNASAN':^65}\n{'='*65}")
        for h in self.data_master["hutang"]:
            warna = HIJAU if h['status'] == "LUNAS" else MERAH
            print(f"Pemberi: {h['pemberi']:<15} | Status: {warna}{h['status']}{PUTIH}")
            print(f"Sisa   : Rp {h['sisa']:,.0f} / Total: Rp {h['nominal']:,.0f}")
            for b in h["bayar"]: print(f"  - {b['tgl']}: Rp {b['nom']:,.0f} (Penerima: {b['pen']})")
            print("-" * 65)
        input("\nEnter...")

    # --- MENU 10: EDIT & HAPUS HUTANG ---
    def menu_perbaikan_hutang(self):
        while True:
            self.banner()
            print(f"{PUTIH}--- Edit & Hapus Data Hutang ---")
            print("1. Edit Data Hutang\n2. Hapus Record Hutang\n3. Kembali")
            p = input(f"\n{HIJAU}Azzkury-ID{PUTIH} > ")
            if p == "3": break
            self.filter_tampilkan_hutang()
            htg = self.data_master["hutang"]
            if not htg: input("Database hutang kosong!"); continue
            try:
                idx = int(input(f"{HIJAU}>>{PUTIH} Pilih Nomor Hutang: ")) - 1
                if 0 <= idx < len(htg):
                    if p == "1":
                        nom = float(input("Nominal Hutang Baru: "))
                        t = input("Tgl: "); b = input("Bln: "); th = input("Thn: ")
                        pemb = input("Pemberi Hutang Baru: ")
                        tgl_v = self.validasi_tanggal(t, b, th)
                        if tgl_v:
                            # Menyesuaikan sisa hutang jika nominal awal berubah
                            selisih = nom - htg[idx]['nominal']
                            htg[idx].update({
                                "nominal": nom,
                                "tgl": tgl_v,
                                "pemberi": pemb,
                                "sisa": max(0, htg[idx]['sisa'] + selisih)
                            })
                            if htg[idx]['sisa'] <= 0: htg[idx]['status'] = "LUNAS"
                            else: htg[idx]['status'] = "BELUM LUNAS"
                            self.save_data()
                    elif p == "2":
                        if input("Yakin hapus data hutang ini? (y/n): ") == "y": htg.pop(idx); self.save_data()
                else: print(f"{MERAH}Nomor tidak valid!{NORMAL}")
            except: print("Error!")
            input("\nEnter...")

def main():
    jarvis = CatatanKeuangan()
    while True:
        jarvis.banner()
        # Layout Menu yang Ditata Ulang (Tengah Balance)
        print(f"{PUTIH} 1. Input Pemasukan             6. Evaluasi Keuangan")
        print(f" 2. Input Pengeluaran            7. Catatan Hutang")
        print(f" 3. Cek Saldo & Riwayat          8. Pelunasan Hutang")
        print(f" 4. Edit & Hapus Data            9. Data Hutang & Pelunasan")
        print(f" 5. Reset Database              10. Edit & Hapus Hutang")
        print(f"\n{PUTIH}                11. Exit System{NORMAL}")
        
        p = input(f"\n{HIJAU}Azzkury-ID{PUTIH} > ")
        if p == "1": jarvis.tambah_transaksi("Pemasukan")
        elif p == "2": jarvis.tambah_transaksi("Pengeluaran")
        elif p == "3": jarvis.tampilkan_total()
        elif p == "4": jarvis.menu_perbaikan()
        elif p == "5":
            if input("Wipe Data? (y/n): ") == "y": jarvis.data_master = {"transaksi":[],"hutang":[]}; jarvis.save_data()
        elif p == "6": jarvis.evaluasi()
        elif p == "7": jarvis.catat_hutang()
        elif p == "8": jarvis.pelunasan_hutang()
        elif p == "9": jarvis.data_hutang_lengkap()
        elif p == "10": jarvis.menu_perbaikan_hutang()
        elif p == "11": 
            jarvis.ketik(f"{HIJAU}[*] Shutdown Jarvis Financial System... Sampai jumpa Tuan Muda Azzkury.")
            break

if __name__ == "__main__":
    main()
