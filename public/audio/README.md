# Rekaman pembelajaran

MP3 rekaman belum dibundel. Tempatkan rekaman guru di folder ini dengan ID dari `data/curriculum.json`.

- `istima-1.mp3`: bacaan lengkap level 1.
- `istima-1-q1.mp3`: pertanyaan 1 level 1.
- `kalam-1.mp3`: dialog pembuka level 1.
- `kalam-1-q1.mp3`: pertanyaan lisan 1 level 1.

Audio harus persis sesuai teks Arab pada ID tersebut. Jangan memecah satu bacaan Istima’ menjadi sepuluh klip. Pastikan seluruh rekaman ditelaah guru dan hak penggunaan rekaman dimiliki pengelola.

Alternatif TTS build-time: `npm run audio:generate` dengan `OPENAI_API_KEY` di server/terminal. Lihat README utama untuk biaya, konfigurasi, dan keterbatasan. Bila file tidak ada, aplikasi memeriksa suara Arab perangkat lalu mencoba server sesuai konfigurasi.
