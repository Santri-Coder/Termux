#!/bin/bash

# -- WARNA --
G='\e[1;32m' # Hijau
W='\e[1;37m' # Putih
N='\e[0m'    # Reset
B='\e[1;34m' # Biru
Y='\e[1;33m' # Kuning
R='\e[1;31m' # Merah

# -- FUNGSI EFEK MENGETIK --
type_effect() {
    local text="$1"
    for (( i=0; i<${#text}; i++ ));
    do
        echo -ne "${text:$i:1}"
        sleep 0.01
    done
}

# -- STAGE 1: LOG AKTIFITAS --
clear
echo -e "${G}[INFO] EXECUTING AZZKURY KERNEL EXPLOIT..."
sleep 0.05
echo -e "${G}[INFO] INJECTING SHELLCODE INTO HYPEROS FRAMEWORK..."
sleep 0.05
echo -e "${G}[INFO] BYPASSING GOOGLE PLAY PROTECT... [DONE]"
sleep 0.05
echo -e "${G}[INFO] TUNNELING VIA PORT 443 -> LOCALHOST..."
sleep 0.05
echo -e "${G}[INFO] ESTABLISHING ENCRYPTED LINK TO SATELLITE-01..."
sleep 0.05
echo -e "${R}[WARN] FIREWALL DETECTED! INITIATING BRUTEFORCE..."
sleep 0.1
echo -e "${G}[INFO] SECURITY OVERRIDE SUCCESSFUL."
sleep 0.05
echo -e "${G}[INFO] LOADING NEURAL ENGINE LLAMA-3.3..."
sleep 0.05
echo -e "${G}[OK] ALL PROTOCOLS ACTIVE. SYSTEM HIJACKED."
sleep 0.4

# -- STAGE 2: MEMBERSIHKAN LAYAR --
clear

# -- STAGE 3: VOICE WELCOME --
if command -v termux-tts-speak &> /dev/null;
then
    termux-tts-speak -p 1.1 -r 1.0 "System Online, Welcome Back Sir Azzkury" &
fi

# -- STAGE 4: BANNER ASCII --
echo -e "${W}  ▐▓█▀▀▀▀▀▀▀▀▀█▓▌  ▄▄▄▄▄   "
echo -e "${W}  ▐▓█${G}Robot${W}🤖  █▓▌  █▄▄▄█ "
echo -e "${W}  ▐▓█  ${G}Jarvis${W} █▓▌  █▄▄▄█   "
echo -e "${W}  ▐▓█▄▄▄▄▄▄▄▄▄█▓▌  █:███   "
echo -e "${W}      ▄▄███▄▄      █████  "

echo -e "${W} ╔══════════════════════════════════════════╗"
echo -ne " ║${B}"
type_effect "              Welcome Back Sir            "
echo -e "${W}║"
echo -e " ╚══════════════════════════════════════════╝"

# -- STAGE 5: QUOTES --
echo ""
QUOTE_DATA=$(curl -sk --connect-timeout 3 "https://zenquotes.io/api/random")
if [ $? -eq 0 ]; then
    TEXT=$(echo $QUOTE_DATA | grep -oP '(?<="q":")[^"]*')
    AUTHOR=$(echo $QUOTE_DATA | grep -oP '(?<="a":")[^"]*')
    echo -ne "${B}Jarvis:${W} "
    type_effect "Hello Sir! This motivation for you today.."
    echo -e "\n${Y}\"$TEXT\"${N}"
    echo -e "${W}— ${AUTHOR}${N}"
else
    echo -ne "${B}Jarvis:${W} "
    type_effect "Sorry Sir! Jarvis can't connecting to satelite..."
fi
echo -e "\n"

# -- MENU TERKUNCI --
echo -e "${B}I'm Jarvis 🤖 please say what do you want?${N}"
echo -e "${W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${N}"
echo -e "${G} [1]${W} Social Media Downloader"
echo -e "${G} [2]${W} Knowledge of Javanese"
echo -e "${G} [3]${W} Database Financial"
echo -e "${G} [x]${W} Exit"
echo ""
read -p " Tentukan pilihanmu, Tuan Muda Azzkury: " opt

case $opt in
  1) python ~/dldsosmed.py ;;
  2) node ~/javanese.js ;;
  3) python ~/finance.py ;;
  x) echo -e "${W} Sistem Shutdown, back to manual terminal${N}" ;;
  *) echo -e "${R} Your prompt is anomali, siste auto shutdown${N}" ;;
esac

# -- PROMPT UTAMA TETAP AKTIF DI BAWAH --
export PS1="\[\e[1;31m\]┌─[\[\e[1;33m\]\$(date +%A)\[\e[1;31m\]]─[\[\e[1;33m\]\$(date +%d-%m-%Y)\[\e[1;31m\]]─[\[\e[1;36m\]\A\[\e[1;31m\]]
\[\e[1;31m\]└─[\[\e[1;37m\]Azzkury\[\e[1;31m\]]──[\[\e[1;33m\]\w\[\e[1;31m\]]─> \[\e[0m\]"
