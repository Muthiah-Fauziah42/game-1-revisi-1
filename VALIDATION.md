# Catatan pemeriksaan — 4 November 2026

## Terverifikasi otomatis

- Build produksi `npm run build`: berhasil (Next.js 16.4.5).
- Pemeriksaan TypeScript: berhasil.
- `npm test`: 9 tes lulus, 0 gagal.
- `npm run validate:content`: 30 level dan 300 pertanyaan.
- Masing-masing dunia: 10 level dan 100 pertanyaan.
- Seluruh materi utama berbeda; seluruh ID pertanyaan unik.
- 200 soal Istima’/Qira’ah memiliki empat opsi berbeda, satu indeks jawaban benar, dan pembahasan Arab/Indonesia.
- 100 soal Kalam memiliki contoh respons, alternatif, kriteria, dan terjemahan pertanyaan.
- Seluruh level memiliki misi, tujuan, enam kosakata, terjemahan materi, dan hadiah.
- Bacaan Istima’ mengikuti rentang panjang yang disarankan: 50–80 / 70–100 / 90–130 / 120–150 kata menurut kelompok level.
- Batas 60/80/90 poin, pembukaan level, skor terbaik, hadiah tanpa duplikasi, serta pemisahan mode demo diperiksa tes.
- Rubrik Kalam 40%/25%/20%/15% diperiksa tes.
- Perpindahan tiga tahap petualangan dan perubahan bab diperiksa tes.
- JSON progres dapat diserialisasi/dipulihkan; data rusak ditolak.
- Endpoint AI tanpa konfigurasi mengembalikan status belum aktif; token salah dan ID materi tidak valid ditolak tanpa panggilan ke penyedia.
- `npm audit --omit=dev --audit-level=high`: tidak menemukan kerentanan pada dependensi produksi saat pemeriksaan.

## Implementasi tersedia, penerimaan perangkat belum selesai

- Tata letak responsif dibuat untuk desktop, tablet, dan ponsel, tetapi interaksi seluruh ukuran layar belum diverifikasi di browser.
- Inspeksi browser dimulai, lalu terhalang kebijakan akses lingkungan. Ini bukan hasil lulus QA browser dan bukan bukti situs target gagal.
- Play/pause/resume/replay, pemilihan suara Arab, mikrofon, MediaRecorder, dan SpeechRecognition memerlukan uji pada browser/perangkat siswa.
- Tidak ada mikrofon fisik atau kunci API yang digunakan untuk verifikasi ini.
- Endpoint penyedia untuk transkripsi, TTS, penilaian, dan tutor telah diimplementasikan; keberhasilan panggilan live belum diuji.
- Rekaman MP3 belum dibundel. Tersedia jalur file rekaman guru, suara Arab perangkat, serta TTS server. Generator MP3 disertakan.
- Telaah ahli Bahasa Arab dan uji pedagogis belum dilakukan; tes struktural tidak membuktikan ketepatan linguistik atau validitas instrumen.

## Status penyerahan

Kode sumber telah dikemas untuk GitHub dan Vercel. Belum diunggah ke repositori pengguna atau dideploy ke akun Vercel. Tidak ada akun/login, sinkronisasi Supabase, atau dashboard kelas daring yang diklaim aktif. README mencakup cara menjalankan, mengaktifkan layanan, menyediakan audio, deploy, dan melakukan pengujian penerimaan.

**Proyek tidak dinyatakan selesai seluruh checklist akhir sampai pemeriksaan perangkat, audio, mikrofon, serta telaah materi dilakukan.**
