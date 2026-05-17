import os
import time
import subprocess
import requests

# Warna ANSI
GRN = "\033[92m" # Hijau
WHT = "\033[97m" # Putih
YLW = "\033[93m" # Kuning
CYAN = "\033[36m" # Cyan
RST = "\033[0m"  # Reset

# User Agent Terbaru
CHROME_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
DOWNLOAD_DIR = "/storage/emulated/0/Download"

def banner():
    os.system('clear')
    print(WHT + "    " + GRN + "▐▓█▀▀▀▀▀▀▀▀▀█▓▌" + WHT + "  " + GRN + "▄▄▄▄▄" + WHT + "      ✧")
    print(WHT + "    " + GRN + "▐▓█" + WHT + "  Tools " + GRN + " █▓▌  " + GRN + "█▄▄▄█" + WHT + "   ╔════════╗")
    print(WHT + "    " + GRN + "▐▓█" + WHT + "Download" + GRN + " █▓▌  " + GRN + "█▄▄▄█" + WHT + "   ║        ║")
    print(WHT + "    " + GRN + "▐▓█▄▄▄▄▄▄▄▄▄█▓▌" + WHT + "  " + GRN + "█:███" + WHT + "   ║        ║")
    print(WHT + "    " + GRN + "░░░░▄▄███▄▄░░░░" + WHT + "  " + GRN + "█████" + WHT + "   ║        ║")
    print(WHT + "  ╔══════════════════════════╣        ║")
    print(WHT + "  ╚══════════════════════════╝        ║")
    print(WHT + "  ╔═══════════════════════════════════╩═════════╗")
    print(WHT + "  ║••••••     " + GRN + "Jarvis Multi-Downloader" + WHT + "     ••••••║")
    print(WHT + "  ╠═════════════════════════════════════════════╣")
    print(WHT + "  ║            " + YLW + " Author: Azzkury" + WHT + "                 ║")
    print(WHT + "  ╠═════════════════════════════════════════════╣")
    print(WHT + "  ║   " + YLW + " Github : https://github.com/Santri-Coder" + WHT + " ║")
    print(WHT + "  ║   " + YLW + " Instagram : Azz.kury" + WHT + "                     ║")
    print(WHT + "  ╚═════════════════════════════════════════════╝")

def get_yt(url, mode):
    import yt_dlp
    output_path = f"{DOWNLOAD_DIR}/%(title)s.%(ext)s"
    
    # Base options yang mengaktifkan progress bar bawaan yt-dlp secara rapi
    opts = {
        'user_agent': CHROME_UA,
        'outtmpl': output_path,
        'noprogress': False,  # Memastikan progress bar tidak disembunyikan
        'quiet': False,       # Mengaktifkan output log download ke terminal
    }
    
    if mode == 'music':
        opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
        })
    else:
        opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })
        
    print(f"\n{CYAN}[+] Menghubungkan ke satelit YouTube...{RST}")
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

def get_social(url, platform):
    import yt_dlp
    output_path = f"{DOWNLOAD_DIR}/%(title)s.%(ext)s"
    print(f"\n{CYAN}[+] Memproses {platform} Original HD...{RST}")
    
    # Menggunakan yt_dlp object langsung via Python agar animasi progress bar muncul alami
    opts = {
        'user_agent': CHROME_UA,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': output_path,
        'no_playlist': True,
        'noprogress': False,
        'quiet': False
    }
    
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        print(f"\n{GRN}[SUCCESS]{RST} {platform} berhasil mendarat di folder Download!")
    except Exception as e:
        print(f"\n[!] Gagal eksekusi, {platform} mungkin memblokir akses atau link tidak valid.")

def get_twitter_mass(url):
    print(f"\n{CYAN}[+] Memindai semua video di tweet (Mass Download)...{RST}")
    try:
        tweet_id = url.split('/')[-1].split('?')[0]
        api_url = f"https://api.vxtwitter.com/status/{tweet_id}"
        response = requests.get(api_url, timeout=15).json()
        if 'media_extended' in response:
            videos = [m for m in response['media_extended'] if m['type'] == 'video']
            if videos:
                print(f"{CYAN}[+] Ditemukan {len(videos)} video! Memulai eksekusi...{RST}")
                for index, vid in enumerate(videos, start=1):
                    video_url = vid['url']
                    output_file = f"{DOWNLOAD_DIR}/X_{tweet_id}_part{index}.mp4"
                    
                    # Dapatkan ukuran file untuk membuat custom progress bar manual ala Termux
                    response_file = requests.get(video_url, stream=True)
                    total_size = int(response_file.headers.get('content-length', 0))
                    
                    print(f"{CYAN}[+] Mendownload video ke-{index}...{RST}")
                    
                    # Logika download dengan progress bar teks dinamis jika content-length tersedia
                    with open(output_file, 'wb') as f:
                        if total_size == 0:
                            f.write(response_file.content)
                        else:
                            downloaded = 0
                            start_time = time.time()
                            for chunk in response_file.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    
                                    # Kalkulasi persentase dan kecepatan
                                    done = int(50 * downloaded / total_size)
                                    percent = (downloaded / total_size) * 100
                                    elapsed = time.time() - start_time
                                    speed = downloaded / elapsed if elapsed > 0 else 0
                                    
                                    # Cetak progress bar manual bergaya terminal bawaan
                                    # Format: [██████████████████▒▒▒▒▒▒▒] 65.2% (512.4 kB/s)
                                    sys.stdout.write(f"\r{WHT}[{GRN}{'█' * done}{WHT}{'░' * (50 - done)}] {GRN}{percent:.1f}%{WHT} ({speed/1024:.1f} kB/s){RST}")
                                    sys.stdout.flush()
                    print() # Pindah baris setelah part selesai
                print(f"\n{GRN}[SUCCESS]{RST} Semua {len(videos)} video diamankan, Tuan Muda!")
            else: print("\n[!] Jarvis tidak nemu video.")
        else: print("\n[!] Metadata tidak ditemukan.")
    except Exception as e: print(f"\n[!] Kendala: {e}")

def main():
    import sys
    global sys
    while True:
        banner()
        print(WHT + "===============================================")
        print(WHT + " Pilih menu anda")
        print(GRN + " 1. " + WHT + "Download music youtube")
        print(GRN + " 2. " + WHT + "Download video youtube")
        print(GRN + " 3. " + WHT + "Download reels instagram")
        print(GRN + " 4. " + WHT + "Download reels facebook")
        print(GRN + " 5. " + WHT + "Download video twitter (Mass)")
        print(GRN + " 6. Exit")
        print(WHT + "===============================================")
        
        pilih = input(WHT + " Pilih (1-6) : " + YLW)
        
        if pilih == '6':
            print(GRN + "\n Jarvis izin pamit standby, Tuan Muda. 😁" + RST)
            break
        
        if pilih not in ['1', '2', '3', '4', '5']:
            print(GRN + "\n Menu tidak valid, Tuan Muda.")
            time.sleep(1)
            continue

        link = input(WHT + " Silahkan masukkan link: " + YLW)
        if not link:
            print(GRN + " Link kosong Tuan Muda.")
            time.sleep(1)
            continue

        try:
            if pilih == '1': get_yt(link, 'music')
            elif pilih == '2': get_yt(link, 'video')
            elif pilih == '3': get_social(link, 'Instagram')
            elif pilih == '4': get_social(link, 'Facebook')
            elif pilih == '5': get_twitter_mass(link)
            
            print(GRN + "\n Eksekusi selesai. Mau lanjut? (y/n)")
            if input(WHT + " >> " + YLW).lower() != 'y': break
        except Exception as e:
            print(WHT + f"\n Terjadi kendala: {e}")
            input("\n Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
