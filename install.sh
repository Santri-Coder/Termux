#!/bin/bash

# -- WARNA --
G='\e[1;32m'
W='\e[1;37m'
N='\e[0m'

clear
echo -e "${G}[+] Menginisiasi Instalasi Menu Jarvis Permanen...${N}"
sleep 1

# 1. Memindahkan file pendukung ke folder home secara permanen
echo -e "${G}[+] Menyalin script ke sistem lokal...${N}"
cp pembuka.sh ~/pembuka.sh
cp jarvisv3.py ~/jarvisv3.py
cp dldsosmed.py ~/dldsosmed.py
cp javanese.js ~/javanese.js
cp finance.py ~/finance.py

# 2. Memberikan izin eksekusi
chmod +x ~/pembuka.sh

# 3. Merombak .bashrc asli agar otomatis memanggil pembuka.sh saat Termux dibuka
echo -e "${G}[+] Mengonfigurasi Layar Utama Termux...${N}"
cat << 'EOF' > ~/.bashrc
#!/bin/bash
# Eksekusi Menu Jarvis Permanen
if [ -f ~/pembuka.sh ]; then
    bash ~/pembuka.sh
fi
EOF

echo -e "${G}[✔] SELESAI! Silahkan restart Termux Tuan Muda.${N}"
