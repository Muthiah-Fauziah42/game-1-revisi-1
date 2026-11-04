# رِحْلَةُ الْمَفْقُودِ — THE LOST EXPEDITION

Website petualangan Bahasa Arab untuk anak SD/MI, usia 7–12 tahun. Proyek **Next.js + TypeScript** untuk repositori GitHub dan deployment Vercel.

## Mulai di komputer

Pasang Node.js 20.9 atau lebih baru (disarankan Node.js 24 LTS), lalu buka terminal pada folder proyek:

```bash
npm ci
npm run dev
```

Buka alamat yang dicetak terminal, biasanya `http://localhost:3000`. Tidak perlu API key untuk membaca materi, menjalankan Qira’ah, merekam Kalam dengan pendampingan guru, atau menyimpan progres. Istima’ membutuhkan suara Arab perangkat, rekaman MP3, atau layanan TTS server.

```bash
npm run typecheck
npm test
npm run validate:content
npm run build
npm start
```

## Isi proyek

| Dunia | Materi utama | Evaluasi |
|---|---|---|
| Istima’ — Hutan Suara | 10 cerita utuh berbeda, 63–125 kata | 100 soal; 4 pilihan per soal |
| Kalam — Kota Percakapan | 10 skenario komunikasi berbeda | 100 pertanyaan lisan; contoh, alternatif, dan kriteria |
| Qira’ah — Kastil Cerita | 10 bacaan utuh berbeda | 100 soal; 4 pilihan per soal |
| Jumlah | 30 level, 30 materi | Tepat 300 pertanyaan |

Materi Arab berharakat, RTL, dan terjemahan Indonesia. Kosakata enam istilah per level. Materi bacaan/pertanyaan adalah konten asli untuk aplikasi ini. Guru tetap perlu menelaah bahasa, kesesuaian pedagogis, distraktor, dan tingkat kesulitan sebelum penggunaan di kelas.

## Alur permainan

- Beranda → pilih dunia → peta 10 misi → materi → 10 pertanyaan berurutan → hasil dan pembahasan.
- Nilai minimal 60 membuka level berikutnya. 60–79 = 1 bintang; 80–89 = 2; 90–100 = 3. Nilai di bawah 60 tetap dicatat.
- Nilai terbaik menentukan penghargaan. Tiap bintang bernilai 20 koin; mengulang level tidak menggandakan koin. Koin adalah koleksi tanpa transaksi.
- Progres dan draf sesi disimpan setiap perubahan dan saat waktu belajar bertambah. Keluar dari sesi menghentikan penghitung waktu aktif. Satu draf aktif per perangkat; memulai level lain menggantikan draf sebelumnya.
- Mode petualangan terpadu memiliki 10 bab; tiap bab melewati Istima’, Kalam, Qira’ah secara berurutan, menggunakan paket kurikulum yang sama dalam cerita pengumpulan gulungan. Bukan tambahan 300 soal lain.
- Pengaturan → Mode demo membuka semua level untuk pemeriksaan. Demo tidak membuka progres nyata atau memberikan penghargaan. Demo Kalam bisa memeriksa contoh respons tanpa mikrofon, diberi label tanpa nilai.
- Progresku menampilkan nilai terbaik, percobaan, jumlah respons, durasi, pemutaran audio, petunjuk, kategori pemahaman, dan rerata rubrik Kalam. Laporan CSV, cadangan JSON, dan pemulihan tersedia.
- Pengaturan bahasa menerjemahkan navigasi utama ke Arab; instruksi pendamping tetap Indonesia sesuai konsep bilingual.

## Struktur folder dan data

```text
app/
  page.tsx                 # entry aplikasi
  layout.tsx               # metadata
  globals.css              # tema, RTL, responsif, Tailwind
  api/
    status/route.ts        # status konfigurasi, tanpa mengungkap rahasia
    speech/route.ts        # TTS materi terdaftar saja
    transcribe/route.ts    # STT rekaman yang disetujui
    evaluate/route.ts      # evaluasi semantik respons Kalam
    tutor/route.ts         # variasi dialog dan rekomendasi sesuai level/nilai
components/
  Expedition.tsx           # beranda, peta, materi, soal, hasil, progres, pengaturan
  Scenery.tsx              # ilustrasi SVG tiga dunia
  AudioPlayer.tsx          # play, pause, resume, replay
  Speaking.tsx             # mikrofon, rekaman, transkrip, rubrik
  Tutor.tsx                # latihan tambahan AI setelah evaluasi
lib/
  types.ts                 # Level, Question, Answer, Draft, Save, Assessment
  game.ts                  # penilaian, unlock, hadiah, validasi cadangan
  server-ai.ts             # guard dan panggilan AI di server
 data/curriculum.json      # 30 level dan 300 pertanyaan
 scripts/build-curriculum.py # sumber penyusunan materi, tanpa dependensi Python tambahan
 scripts/generate-audio.mjs  # pembuatan MP3 opsional lewat API berbayar
 tests/                   # pemeriksaan kurikulum, progres, rubrik, API guard
 public/fonts/            # Amiri lokal, lisensi SIL OFL disertakan
 public/audio/            # tempat rekaman guru atau audio TTS yang dibuat pengelola
```

`Level` menyimpan ID, dunia, nomor, judul, tujuan, misi, tokoh, teks Arab, terjemahan, kosakata, kesulitan, benda hadiah, dan array **10** `Question`.

Soal Istima’/Qira’ah memiliki `options[4]`, `answer` (indeks 0–3), kategori, bukti kalimat Arab, dan pembahasan Indonesia. Soal Kalam memiliki pertanyaan, terjemahan, `example`, `alternatives`, serta `criteria`. Data dan logika terpisah dari komponen tampilan. Regenerasi kurikulum dengan `python3 scripts/build-curriculum.py` lalu jalankan tes.

## Audio Istima’ dan pertanyaan Kalam

Urutan sumber audio:

1. File rekaman lokal `public/audio/<id>.mp3`.
2. Web Speech Synthesis dengan **suara Arab yang benar-benar terdeteksi**, bukan asumsi semua browser mendukungnya.
3. TTS server setelah kunci dan token akses dikonfigurasi.

ID cerita contoh: `istima-1.mp3`. ID pertanyaan: `istima-1-q1.mp3`, `kalam-1-q1.mp3`. Skenario pembuka Kalam opsional: `kalam-1.mp3`. Pemutaran ulang bacaan memakai file cerita yang sama. Istima’ baru membuka evaluasi setelah audio utama selesai; transkrip dan terjemahan cerita tidak dibuka sampai semua soal selesai. Qira’ah menampilkan teks selama evaluasi tetapi menyembunyikan terjemahan lengkap hingga hasil.

**MP3 rekaman belum dibundel.** Jika perangkat tidak memiliki suara Arab dan server belum dikonfigurasi, audio menampilkan pesan bantuan; tidak berpura-pura telah diputar. Demi audio yang konsisten lintas perangkat, rekam materi bersama guru atau jalankan generator TTS lalu telaah hasilnya:

```bash
# Setelah OPENAI_API_KEY terpasang pada lingkungan terminal:
npm run audio:generate
```

Generator menghasilkan 220 file: 10 bacaan Istima’, 100 pertanyaan Istima’, 10 pembuka Kalam, dan 100 pertanyaan Kalam. File yang sudah ada dilewati agar bisa melanjutkan setelah terhenti. API dapat berbayar; jalankan hanya saat siap menggunakan akun API pengelola. Suara TTS adalah suara buatan AI, bukan rekaman manusia. Model dapat diganti melalui environment variable; periksa ketersediaan model dan dokumentasi penyedia saat mengaktifkan layanan.

## Kalam: rekaman, transkripsi, dan penilaian

- Mikrofon hanya aktif setelah anak menekan tombol dan browser memberikan izin. Membutuhkan HTTPS atau localhost dan browser dengan MediaRecorder.
- Batas satu rekaman 60 detik; selesai merekam menghentikan stream mikrofon. Tombol putar tersedia untuk memeriksa respons sendiri.
- SpeechRecognition `ar-SA` dipakai jika browser mendukungnya. Implementasi browser bisa mengirim suara ke layanan pengenalan milik penyedia browser; ini dinyatakan pada UI. Suara dan nama lengkap tidak disimpan dalam progres.
- Transkripsi server tidak otomatis: perlu centang persetujuan bersama guru/orang tua, token akses, dan server terkonfigurasi. Rekaman maksimum 4 MB. Audio hanya berada sementara di browser, dikirim ke penyedia saat tombol transkripsi server ditekan, dan tidak disimpan oleh aplikasi di server.
- Evaluasi AI mengirim pertanyaan dan transkrip yang disetujui, dengan kriteria kurikulum serta konteks respons sebelumnya. Nama panggilan profil tidak dikirim. Tidak memaksa respons sama persis dengan contoh.
- Rubrik: relevansi 40%, kosakata 25%, struktur 20%, keterpahaman 15%; tiap soal maksimum 10 poin. AI menilai **keterpahaman teks hasil transkripsi**, bukan analisis pelafalan. Penilaian guru mendengarkan rekaman langsung.
- Jika AI tidak dikonfigurasi, guru/pendamping memilih “Nilai bersama guru”, mendengarkan rekaman, dan mengisi empat aspek rubrik. Tidak ada nilai AI palsu, pencocokan kata yang diklaim sebagai penilaian semantik, atau nilai otomatis dari rekaman yang belum dikenali.
- Contoh jawaban Kalam dalam evaluasi baru tersedia setelah respons direkam dan penilaian guru dibuka; mode demo dilabeli terpisah.

## Mengaktifkan server AI

Salin `.env.example` menjadi `.env.local` untuk pengembangan. Di Vercel, isi melalui **Project Settings → Environment Variables**, bukan melalui kode:

```dotenv
OPENAI_API_KEY=diisi_di_server_saja
OPENAI_TEXT_MODEL=gpt-4.1-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TRANSCRIBE_MODEL=gpt-4o-mini-transcribe
AI_ACCESS_TOKEN=token_acak_panjang_khusus_guru
```

Semua panggilan penyedia ada pada API Routes. Tidak ada rahasia dengan awalan `NEXT_PUBLIC_`. Setelah server dikonfigurasi, guru memasukkan token akses melalui Pengaturan → Layanan AI pada sesi perangkat. Token hanya disimpan di sessionStorage dan tidak ikut cadangan progres.

Endpoint berbayar menolak permintaan bila konfigurasi/token belum sesuai, membatasi ID materi, ukuran input, serta jumlah permintaan dasar (15/menit/IP per instance). Pembatas memori bukan kuota global yang tahan restart. Untuk penggunaan publik berskala besar, ganti token guru bersama dengan autentikasi guru/siswa dan rate limiter terdistribusi; batasi anggaran API di penyedia. Prototipe ini tidak memiliki login atau pengelolaan kelas daring.

Endpoint tutor memberi variasi dialog, penjelasan Indonesia, dan rekomendasi latihan yang mengikuti level/nilai. Latihan tambahan tidak mengganti 300 soal utama. Hasil AI tetap perlu pengawasan guru.

Referensi implementasi penyedia:

- [Audio Speech API](https://developers.openai.com/api/reference/resources/audio/subresources/speech/methods/create)
- [Audio Transcription API](https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create)

## Upload ke GitHub

1. Ekstrak ZIP proyek.
2. Buat repositori GitHub baru kosong.
3. Unggah **isi folder proyek**, termasuk `package.json`, `package-lock.json`, `app`, `components`, `data`, `lib`, `public`, `scripts`, `tests`, dan konfigurasi. Jangan unggah `node_modules`, `.next`, atau `.env.local`.
4. Jika menggunakan Git di terminal:

```bash
git init
git add .
git commit -m "Build The Lost Expedition Arabic learning game"
git branch -M main
git remote add origin URL_REPOSITORI_GITHUB_ANDA
git push -u origin main
```

Ganti `URL_REPOSITORI_GITHUB_ANDA` dengan URL repo milik Anda. `.gitignore` sudah mengabaikan dependensi, hasil build, dan rahasia lokal. GitHub Actions memeriksa tipe, tes, struktur konten, serta build pada push/pull request.

## Deploy ke Vercel

1. Masuk Vercel → Add New Project → Import repositori GitHub.
2. Framework Preset: **Next.js**. Root Directory: folder yang berisi `package.json` (biasanya `/` bila isi ZIP diunggah langsung ke root repositori).
3. Install Command: `npm ci`. Build Command: `npm run build`. Output Directory: biarkan default Next.js. Gunakan runtime Node.js 24 bila tersedia.
4. Tambahkan variabel AI bila akan memakai fitur server. Tanpa variabel tersebut, situs tetap berjalan dengan fungsi lokal dan keterangan layanan belum aktif.
5. Klik Deploy. Perubahan yang didorong ke branch produksi akan memicu deployment berikutnya sesuai pengaturan Vercel.
6. Pada URL HTTPS hasil deployment, jalankan pemeriksaan perangkat berikut sebelum digunakan siswa.

## Checklist penerimaan di perangkat nyata

Tes otomatis **tidak menggantikan** pengujian perangkat. Lingkungan pengembangan tidak menyediakan mikrofon fisik siswa atau kredensial API; audio, izin mikrofon, dan endpoint penyedia berbayar belum diverifikasi end-to-end. Pemeriksaan interaksi browser pengembangan juga terhalang kebijakan akses browser; belum ada klaim lulus pengujian browser menyeluruh.

- [ ] Desktop, tablet, dan ponsel: cek teks Arab, ukuran tombol, scroll, dan pergantian halaman.
- [ ] Istima’: putar cerita penuh, jeda, lanjut, ulang; evaluasi tetap terkunci sebelum audio selesai.
- [ ] Jawab 10 soal; nilai benar, transkrip baru terbuka di hasil; coba skor 50/60/80/90.
- [ ] Qira’ah: bacaan tetap tersedia dan terjemahan penuh tidak terlihat selama soal.
- [ ] Kalam: izinkan/tolak mikrofon, rekam, dengarkan ulang, uji respons Arab; matikan jaringan/layanan untuk menguji fallback guru.
- [ ] Jika API diaktifkan: uji token salah/benar, transkripsi, penilaian alternatif jawaban, dan rekomendasi tutor.
- [ ] Refresh browser, lanjutkan draf, ulang level; pastikan bintang tidak terduplikasi dan skor terbaik tidak menurun.
- [ ] Jalankan tiga tahap petualangan; tahap lanjut hanya setelah lulus, demo tidak membuka apa pun.
- [ ] Unduh dan pulihkan cadangan JSON; unduh laporan CSV.
- [ ] Telaah seluruh 30 materi dan 300 pertanyaan bersama guru Bahasa Arab.

## Batas implementasi dan pengembangan berikutnya

Progres bersifat per browser/per perangkat. Sinkronisasi lintas perangkat, dashboard guru daring, akun, dan Supabase **belum diaktifkan**. Untuk pengembangan database, entitas `Attempt`, `Answer`, dan `Save` sudah dipisahkan; tahap berikutnya menambahkan autentikasi, tabel profil/percobaan/jawaban, RLS berbasis pemilik, serta migrasi progres lokal dengan persetujuan pengguna. Jangan mengekspos service-role key Supabase ke browser.

Semua 30 level dan 300 soal tersedia; tidak ada soal placeholder. Namun proyek **belum dinyatakan lulus seluruh checklist akhir** sampai audio, mikrofon, API yang dipakai, dan responsivitas telah diuji pada perangkat target serta telaah materi selesai.
