const symbols = {
    banner: `
  ▐▓█▀▀▀▀▀▀▀▀▀█▓▌  ▄▄▄▄▄
  ▐▓█ꦗꦮ ꦱꦢꦪ   █▓▌  █▄▄▄█
  ▐▓█ilmu jowo█▓▌  █▄▄▄█
  ▐▓█▄▄▄▄▄▄▄▄▄█▓▌  █:███
      ▄▄███▄▄      █████
 ╔═════════════════════════════════════════╗
 ║         Java script weton               ║
 ╚═════════════════════════════════════════╝
    `
};

const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const HIJAU = "\x1b[32m";
const PUTIH = "\x1b[37m";
const RESET = "\x1b[0m";

const dinoArray = ["NGAHAD", "SENEN", "SELASA", "REBO", "KEMIS", "JEMUWAH", "SETU"];
const pasaranArray = ["LEGI", "PAHING", "PON", "WAGE", "KLIWON"];
const neptuDino = { "NGAHAD": 5, "SENEN": 4, "SELASA": 3, "REBO": 7, "KEMIS": 8, "JEMUWAH": 6, "SETU": 9 };
const neptuPasaran = { "LEGI": 5, "PAHING": 9, "PON": 7, "WAGE": 4, "KLIWON": 8 };

function getHijriManual(date) {
    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();
    if (month <= 2) { year -= 1; month += 12; }
    let a = Math.floor(year / 100);
    let b = 2 - a + Math.floor(a / 4);
    let jd = Math.floor(365.25 * (year + 4716)) + Math.floor(30.6001 * (month + 1)) + day + b - 1524.5;
    let l = Math.floor(jd + 1) - 1948440 + 10632;
    let n = Math.floor((l - 1) / 10631);
    l = l - 10631 * n + 354;
    let j = (Math.floor((10985 - l) / 5316)) * (Math.floor((50 * l) / 17719)) + (Math.floor(l / 5670)) * (Math.floor((43 * l) / 15238));
    l = l - (Math.floor((30 - j) / 15)) * (Math.floor((17719 * j) / 50)) - (Math.floor(j / 16)) * (Math.floor((15238 * j) / 43)) + 29;
    let m_h = Math.floor((24 * l) / 709);
    let d_h = l - Math.floor((709 * m_h) / 24);
    let y_h = 30 * n + j - 30;
    const bulanH = ["MUHARRAM", "SAFAR", "RABIUL AWAL", "RABIUL AKHIR", "JUMADIL AWAL", "JUMADIL AKHIR", "RAJAB", "SYAKBAN", "RAMADHAN", "SYAWAL", "ZULKAIDAH", "ZULHIJAH"];
    return { day: d_h, month: bulanH[m_h - 1], year: y_h, full: `${d_h} ${bulanH[m_h - 1]} ${y_h}` };
}

function getWetonOnly(date) {
    const dayIndex = date.getDay();
    const baseDate = new Date(2000, 1, 19);
    const diffDays = Math.floor((date.getTime() - baseDate.getTime()) / (1000 * 3600 * 24));
    let pasaranIndex = (4 + (diffDays % 5 + 5) % 5) % 5;
    return `${dinoArray[dayIndex]} ${pasaranArray[pasaranIndex]}`;
}

function getFullData(date) {
    const hijri = getHijriManual(date);
    const weton = getWetonOnly(date);
    const masehi = date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' }).toUpperCase();
    return `${hijri.full}, ${weton}, ${masehi}`;
}

function cariMendhak(geblagDate, tahunKe) {
    const gH = getHijriManual(geblagDate);
    let target = new Date(geblagDate);
    target.setDate(target.getDate() + (tahunKe * 350));
    while (true) {
        let tH = getHijriManual(target);
        if (tH.day === gH.day && tH.month === gH.month) return target;
        target.setDate(target.getDate() + 1);
        if (target.getFullYear() > geblagDate.getFullYear() + tahunKe + 1) break;
    }
}

function hitungWeton(tgl, bln, thn) {
    const date = new Date(parseInt(thn), parseInt(bln) - 1, parseInt(tgl));
    const dayIndex = date.getDay();
    const baseDate = new Date(2000, 1, 19);
    const diffDays = Math.floor((date.getTime() - baseDate.getTime()) / (1000 * 3600 * 24));
    let pasaranIndex = (4 + (diffDays % 5 + 5) % 5) % 5;
    const d = dinoArray[dayIndex];
    const p = pasaranArray[pasaranIndex];
    return { dino: d, pasaran: p, total: neptuDino[d] + neptuPasaran[p] };
}

function getJodoData(total) {
    const hasil = [
        { nama: "SUJANAN", rejeki: "Rejeki cenderung seret di awal, sering bocor untuk hal tak terduga.", tirakat: "Sering sedekah weton dan puasa Senin-Kamis untuk menolak bala." },
        { nama: "WASESO SEGORO", rejeki: "Lancar mengalir bagai air laut, berwibawa dan disegani.", tirakat: "Menjaga rendah hati dan rutin menyantuni anak yatim." },
        { nama: "PEGAT", rejeki: "Banyak hambatan ekonomi, rawan perselisihan masalah uang.", tirakat: "Puasa mutih pada hari kelahiran masing-masing pasangan." },
        { nama: "RATU", rejeki: "Sangat mapan, dihargai orang banyak, rejeki kelas tinggi.", tirakat: "Selamatan tumpeng nasi kuning setiap tahun perkawinan." },
        { nama: "JODO", rejeki: "Harmonis membawa berkah, rejeki datang dari kerja sama yang baik.", tirakat: "Sholat malam (Tahajud) berjamaah secara rutin." },
        { nama: "TOPO", rejeki: "Awalnya berat dan prihatin, namun sukses di hari tua.", tirakat: "Berhemat (cegah maem) dan rajin puasa weton." },
        { nama: "TINARI", rejeki: "Selalu cukup, sering mendapat keberuntungan tak terduga.", tirakat: "Memperbanyak rasa syukur dan ziarah ke leluhur." },
        { nama: "PADU", rejeki: "Rejeki sedang, namun sering habis untuk biaya meredam masalah.", tirakat: "Latihan sabar (puasa bicara kotor) dan shodaqoh harian." }
    ];
    return hasil[total % 8];
}

function getPrimbonPitu(total) {
    const daftar = [
        { nama: "LEBU KATIUP ANGIN", watak: "Sering mengalami kesusahan, cita-cita sulit tercapai, sering pindah tempat." },
        { nama: "WASESO SEGORO", watak: "Pemaaf, berwibawa, berwawasan luas, and murah rezeki." },
        { nama: "TUNGGAK SEMI", watak: "Mudah mendapatkan rezeki dan keberuntungan selalu mengalir." },
        { nama: "SUMUR SINABA", watak: "Menjadi tempat pengungsian/bertanya, bijaksana, dan banyak ilmu." },
        { nama: "SATRIO WIBAWO", watak: "Selalu mendapatkan kemuliaan, dihormati, dan beruntung." },
        { nama: "BUMI KAPETAK", watak: "Suka bekerja keras, kuat menahan cobaan, tapi sering dihina." },
        { nama: "SATRIO WIRANG", watak: "Sering mendapat malu, rintangan cukup banyak, namun sabar." },
        { nama: "SANGGAR WARINGIN", watak: "Teduh, memberi perlindungan, berkembang, tenteram, dan bahagia." }
    ];
    let index = total % 7;
    if (index === 0) index = 7;
    return daftar[index];
}

function getZodiak(d, m) {
    if ((m == 3 && d >= 21) || (m == 4 && d <= 19)) return { n: "ARIES", w: "Aktif, inisiatif, suka tantangan, dan punya jiwa pemimpin." };
    if ((m == 4 && d >= 20) || (m == 5 && d <= 20)) return { n: "TAURUS", w: "Sabar, setia, penyayang, namun terkadang keras kepala." };
    if ((m == 5 && d >= 21) || (m == 6 && d <= 20)) return { n: "GEMINI", w: "Komunikatif, cerdas, mudah bergaul, dan sangat adaptif." };
    if ((m == 6 && d >= 21) || (m == 7 && d <= 22)) return { n: "CANCER", w: "Emosional, protektif, intuitif, dan sangat mencintai keluarga." };
    if ((m == 7 && d >= 23) || (m == 8 && d <= 22)) return { n: "LEO", w: "Percaya diri, optimis, murah hati, dan senang menjadi pusat perhatian." };
    if ((m == 8 && d >= 23) || (m == 9 && d <= 22)) return { n: "VIRGO", w: "Praktis, kritis, perfeksionis, dan suka membantu orang lain." };
    if ((m == 9 && d >= 23) || (m == 10 && d <= 22)) return { n: "LIBRA", w: "Diplomatis, menyukai harmoni, adil, dan punya cita rasa seni." };
    if ((m == 10 && d >= 23) || (m == 11 && d <= 21)) return { n: "SCORPIO", w: "Tekun, ambisius, setia, namun sangat misterius dan tertutup." };
    if ((m == 11 && d >= 22) || (m == 12 && d <= 21)) return { n: "SAGITTARIUS", w: "Suka kebebasan, jujur, optimis, dan gemar berpetualang." };
    if ((m == 12 && d >= 22) || (m == 1 && d <= 19)) return { n: "CAPRICORN", w: "Bertanggung jawab, disiplin, sabar, dan sangat berorientasi pada tujuan." };
    if ((m == 1 && d >= 20) || (m == 2 && d <= 18)) return { n: "AQUARIUS", w: "Mandiri, cerdas, progresif, dan memiliki pemikiran yang orisinal." };
    if ((m == 2 && d >= 19) || (m == 3 && d <= 20)) return { n: "PISCES", w: "Imajinatif, peka, artistik, dan memiliki empati yang sangat tinggi." };
}

function getShio(y) {
    const shioList = [
        { n: "MONYET", w: "Cerdas, cerdik, lucu, dan pandai memecahkan masalah sulit." },
        { n: "AYAM", w: "Pekerja keras, percaya diri, pemberani, dan pandai berkomunikasi." },
        { n: "ANJING", w: "Setia, jujur, tulus, dan memiliki rasa keadilan yang tinggi." },
        { n: "BABI", w: "Jujur, murah hati, penyabar, dan sangat menikmati hidup." },
        { n: "TIKUS", w: "Cerdas, mudah beradaptasi, ambisius, dan sangat berhemat." },
        { n: "KERBAU", w: "Kuat, tekun, dapat diandalkan, dan sangat memegang janji." },
        { n: "MACAN", w: "Berani, kompetitif, penuh gairah, dan memiliki kharisma tinggi." },
        { n: "KELINCI", w: "Lembut, sopan, waspada, dan sangat cinta damai." },
        { n: "NAGA", w: "Kuat, bangga, ambisius, dan penuh dengan energi positif." },
        { n: "ULAR", w: "Bijaksana, misterius, tenang, namun memiliki insting yang tajam." },
        { n: "KUDA", w: "Energik, mandiri, suka kebebasan, dan pandai bersosialisasi." },
        { n: "KAMBING", w: "Lembut, artistik, kreatif, dan memiliki hati yang penyayang." }
    ];
    return shioList[y % 12];
}

function menuUtama() {
    console.clear();
    process.stdout.write(`${HIJAU}${symbols.banner}\n`);
    process.stdout.write(`SUGENG RAWUH MONGGO PINARAK, TUAN\n`);
    process.stdout.write(`\nMONGGO MILIH :\n`);
    process.stdout.write(`1. KINAWERUH ETUNGAN WETON\n2. KINAWERUH ETUNGAN PRIMBON\n3. KINAWERUH ETUNGAN JODO\n4. BUKU WETON\n5. BUKU ETUNGAN JODO\n6. ETUNGAN SELAMATAN & TAHLILAN\n7. HAUL TAUNAN\n8. ETUNGAN WETON, ZODIAK, SHIO\n9. METU\n10. PERINGATAN${RESET}\n`);

    rl.question(`\nMILIH NOMER PINTEN : `, (pilihan) => {
        if (pilihan === '1' || pilihan === '2') {
            process.stdout.write(`\n${PUTIH}ISI TANGGAL (conto 28/1/1999)${RESET}\n`);
            rl.question("TANGGAL: ", (t) => {
                rl.question("WULAN: ", (w) => {
                    rl.question("TAUN: ", (th) => {
                        const res = hitungWeton(t, w, th);
                        process.stdout.write(`\n${HIJAU}NIKI HASILE :\n`);
                        if (pilihan === '1') {
                            process.stdout.write(`DINA : ${PUTIH}${res.dino}\n`);
                            process.stdout.write(`${HIJAU}PASARAN : ${PUTIH}${res.pasaran}\n`);
                            process.stdout.write(`${HIJAU}TOTAL NEPTU : ${PUTIH}${res.total}${RESET}\n`);
                        } else {
                            const primbon = getPrimbonPitu(res.total);
                            process.stdout.write(`NEPTU : ${PUTIH}${res.total} ${res.dino} ${res.pasaran}\n`);
                            process.stdout.write(`${HIJAU}PRIMBON : ${PUTIH}${primbon.nama}\n`);
                            process.stdout.write(`${HIJAU}WATAK : ${PUTIH}${primbon.watak}${RESET}\n`);
                        }
                        rl.question(`\n${HIJAU}MBALIK MENU AWAL y/n : ${RESET}`, (ans) => { if (ans.toLowerCase() === 'y') menuUtama(); else process.exit(); });
                    });
                });
            });
        } else if (pilihan === '3') {
            process.stdout.write(`\n${PUTIH}ISI TANGGAL LAIRMU LAN CALON JODOMU\n\n`);
            process.stdout.write(`TANGGAL LAIRMU\n`);
            rl.question("TANGGAL : ", (t1) => {
                rl.question("WULAN : ", (w1) => {
                    rl.question("TAUN : ", (th1) => {
                        process.stdout.write(`\n${PUTIH}TANGGAL LAIR CALONMU\n`);
                        rl.question("TANGGAL : ", (t2) => {
                            rl.question("WULAN : ", (w2) => {
                                rl.question("TAUN : ", (th2) => {
                                    const res1 = hitungWeton(t1, w1, th1);
                                    const res2 = hitungWeton(t2, w2, th2);
                                    const totalGabung = res1.total + res2.total;
                                    const jodo = getJodoData(totalGabung);
                                    process.stdout.write(`\n${HIJAU}NIKI HASILE :\n`);
                                    process.stdout.write(`WETON PANJENENGAN : ${PUTIH}${res1.dino} ${res1.pasaran} (${res1.total})\n`);
                                    process.stdout.write(`${HIJAU}WETON CALON PANJENENGAN : ${PUTIH}${res2.dino} ${res2.pasaran} (${res2.total})\n`);
                                    process.stdout.write(`${HIJAU}CACAHE WETONG GABUNGAN : ${PUTIH}${totalGabung}\n`);
                                    process.stdout.write(`${HIJAU}PRIMBON JODO : ${PUTIH}${jodo.nama}\n`);
                                    process.stdout.write(`${HIJAU}REJEKI : ${PUTIH}${jodo.rejeki}\n`);
                                    process.stdout.write(`${HIJAU}TIRAKATAN : ${PUTIH}${jodo.tirakat}${RESET}\n`);
                                    rl.question(`\n${HIJAU}MBALIK MENU AWAL y/n : ${RESET}`, (ans) => { if (ans.toLowerCase() === 'y') menuUtama(); else process.exit(); });
                                });
                            });
                        });
                    });
                });
            });
        } else if (pilihan === '4') {
            process.stdout.write(`\n${HIJAU}DAFTAR NEPTU WETON :\n`);
            const hArray = ["SELASA", "REBO", "KEMIS", "JEMUWAH", "SETU", "NGAHAD", "SENEN"];
            const pArray = ["WAGE", "LEGI", "PON", "PAHING", "KLIWON"];
            let count = 1;
            hArray.forEach(h => {
                pArray.forEach(p => {
                    const nD = neptuDino[h];
                    const nP = neptuPasaran[p];
                    const total = nD + nP;
                    const labelHutama = `${count}. Neptu ${h} + ${p}`.padEnd(28);
                    process.stdout.write(`${HIJAU}${labelHutama} : ${PUTIH}${total}\n`);
                    const labelRincian = `${h.charAt(0) + h.slice(1).toLowerCase()} ${nD} + ${p.charAt(0) + p.slice(1).toLowerCase()} ${nP}`.padEnd(28);
                    process.stdout.write(`${PUTIH}${labelRincian} : ${total}\n`);
                    count++;
                });
            });
            rl.question(`\n${HIJAU}MBALIK MENU AWAL y/n : ${RESET}`, (ans) => { if (ans.toLowerCase() === 'y') menuUtama(); else process.exit(); });
        } else if (pilihan === '5') {
            process.stdout.write(`\n${HIJAU}TABEL PRIMBON PERJODOHAN (144) :\n`);
            let baris = 1;
            for (let i = 7; i <= 18; i++) {
                for (let j = 7; j <= 18; j++) {
                    const totalJodo = i + j;
                    const labelJodo = `${baris}. Neptu ${i} + Neptu ${j}`.padEnd(28);
                    process.stdout.write(`${HIJAU}${labelJodo} : ${PUTIH}${totalJodo}, ${getJodoData(totalJodo).nama}\n`);
                    baris++;
                }
            }
            rl.question(`\n${HIJAU}MBALIK MENU AWAL y/n : ${RESET}`, (ans) => { if (ans.toLowerCase() === 'y') menuUtama(); else process.exit(); });
        } else if (pilihan === '6') {
            process.stdout.write(`\n${PUTIH}ISI TANGGAL MENINGGAL (conto 28/1/1999)${RESET}\n`);
            rl.question("TANGGAL: ", (t) => {
                rl.question("WULAN: ", (w) => {
                    rl.question("TAUN: ", (th) => {
                        const date = new Date(parseInt(th), parseInt(w) - 1, parseInt(t));
                        process.stdout.write(`\n${HIJAU}NIKI ETUNGAN SELAMATANIPUN :\n`);
                        const list = [
                            { n: "GEBLAG (H-Meninggal)", d: 0 }, { n: "3 DINA (nelungdino)", d: 2 }, { n: "7 DINA (mitungdino)", d: 6 },
                            { n: "40 DINA (Matangpuluh)", d: 39 }, { n: "100 DINA (Nyatus)", d: 99 },
                            { n: "MENDHAK 1", type: "mendhak", y: 1 }, { n: "MENDHAK 2", type: "mendhak", y: 2 }, { n: "1000 DINA (Nyewu)", d: 999 }
                        ];
                        list.forEach(s => {
                            let target = (s.type === "mendhak") ? cariMendhak(date, s.y) : new Date(date);
                            if (!s.type) target.setDate(date.getDate() + s.d);
                            process.stdout.write(`${HIJAU}${s.n.padEnd(25)} : ${PUTIH}${getFullData(target)}\n`);
                        });
                        rl.question(`\n${HIJAU}MBALIK MENU AWAL y/n : ${RESET}`, (ans) => { if (ans.toLowerCase() === 'y') menuUtama(); else process.exit(); });
                    });
                });
            });
        } else if (pilihan === '7') {
            process.stdout.write(`\n${PUTIH}TULIS TANGGAL SEDO\n`);
            rl.question("TANGGAL: ", (t) => {
                rl.question("WULAN: ", (w) => {
                    rl.question("TAHUN: ", (th) => {
                        rl.question("HAUL TAUN : ", (ht) => {
                            const dateSedo = new Date(parseInt(th), parseInt(w) - 1, parseInt(t));
                            const hSedo = getHijriManual(dateSedo);
                            let targetDate = new Date(parseInt(ht), 0, 1);
                            let found = false;
                            for (let i = 0; i < 400; i++) {
                                let hTarget = getHijriManual(targetDate);
                                if (hTarget.day === hSedo.day && hTarget.month === hSedo.month) { found = true; break; }
                                targetDate.setDate(targetDate.getDate() + 1);
                            }
                            process.stdout.write(`\n${HIJAU}NIKI HASILE :\n`);
                            process.stdout.write(`TANGGAL SEDO : ${PUTIH}${dateSedo.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' }).toUpperCase()}\n`);
                            process.stdout.write(`${HIJAU}TAHUN HIJRIAH : ${PUTIH}${hSedo.full}\n`);
                            process.stdout.write(`${HIJAU}TAHUN HAUL: ${PUTIH}${ht}\n`);
                            if (found) {
                                process.stdout.write(`${HIJAU}TANGGAL : ${PUTIH}${targetDate.toLocaleDateString('id-ID', { day: 'numeric', month: 'long' }).toUpperCase()}\n`);
                                process.stdout.write(`${HIJAU}HIJRIAH : ${PUTIH}${getHijriManual(targetDate).full}${RESET}\n`);
                            }
                            rl.question(`\n${HIJAU}MBALIK MENU AWAL y/n : ${RESET}`, (ans) => { if (ans.toLowerCase() === 'y') menuUtama(); else process.exit(); });
                        });
                    });
                });
            });
        } else if (pilihan === '8') {
            process.stdout.write(`\n${PUTIH}ETUNGAN GABUNGAN WETON, ZODIAK, SHIO\nISI TANGGAL LAIR\n`);
            rl.question("TANGGAL: ", (t) => {
                rl.question("WULAN: ", (w) => {
                    rl.question("TAUN: ", (th) => {
                        const date = new Date(parseInt(th), parseInt(w) - 1, parseInt(t));
                        const resWeton = hitungWeton(t, w, th);
                        const resPrimbon = getPrimbonPitu(resWeton.total);
                        const resZodiak = getZodiak(parseInt(t), parseInt(w));
                        const resShio = getShio(parseInt(th));

                        process.stdout.write(`\n${HIJAU}TANGGAL LAIRMU : ${PUTIH}${date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' }).toUpperCase()}\n\n`);
                        process.stdout.write(`${HIJAU}WETON: ${PUTIH}${resWeton.dino} ${resWeton.pasaran} (${resWeton.total})\n`);
                        process.stdout.write(`${HIJAU}WATAK MITURUT WETON: ${PUTIH}${resPrimbon.watak}\n\n`);
                        process.stdout.write(`${HIJAU}ZODIAK: ${PUTIH}${resZodiak.n}\n`);
                        process.stdout.write(`${HIJAU}WATAK MITURUT ZODIAK: ${PUTIH}${resZodiak.w}\n\n`);
                        process.stdout.write(`${HIJAU}SHIO: ${PUTIH}${resShio.n}\n`);
                        process.stdout.write(`${HIJAU}WATAK MITURUT SHIO: ${PUTIH}${resShio.w}${RESET}\n`);
                        rl.question(`\n${HIJAU}MBALIK MENU AWAL y/n : ${RESET}`, (ans) => { if (ans.toLowerCase() === 'y') menuUtama(); else process.exit(); });
                    });
                });
            });
        } else if (pilihan === '9') {
            process.exit();
        } else if (pilihan === '10') {
            process.stdout.write(`\n${HIJAU}!!! PERINGATAN !!!\n`);
            process.stdout.write(`${PUTIH}Semua pengetahuan ini hanya sebatas penambah wawasan\n`);
            process.stdout.write(`Segala takdir dan kepastian rejeki dll.\n`);
            process.stdout.write(`Kita kembalikan pada sang pencipta.\n`);
            process.stdout.write(`Pengetahuan ini hanya sebatas "CUKUP TAHU" \n`);
            process.stdout.write(`Bukan untuk di imani atau di yakini 100%\n`);
            process.stdout.write(`Tetap kembali ber-ikhtiyar, berusaha, dan berdoa.\n`);
            process.stdout.write(`Segala bentuk kecocokan watak, rejeki dll.\n`);
            process.stdout.write(`hanya kebetulan semata\n`);
            process.stdout.write(`Untuk perhitungan SELAMATAN & TAHLILAN dan HAUL TAHUNAN.\n`);
            process.stdout.write(`kami buat berdasarkan hitungan matematika.\n`);
            process.stdout.write(`Insyaallah akurat\n`);
            process.stdout.write(`Jika ada yang meleset kami mohon maaf${RESET}\n`);
            rl.question(`\n${HIJAU}MBALIK MENU AWAL y/n : ${RESET}`, (ans) => { if (ans.toLowerCase() === 'y') menuUtama(); else process.exit(); });
        } else {
            menuUtama();
        }
    });
}

menuUtama();