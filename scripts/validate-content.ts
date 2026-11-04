import { levels } from "../lib/game";
const summary = ["istima", "kalam", "qiraah"].map((w) => ({
  world: w,
  levels: levels.filter((l) => l.world === w).length,
  questions: levels
    .filter((l) => l.world === w)
    .reduce((n, l) => n + l.questions.length, 0),
  words: levels
    .filter((l) => l.world === w)
    .map((l) => l.textAr.split(/\s+/).length),
}));
for (const row of summary)
  if (row.levels !== 10 || row.questions !== 100)
    throw new Error("Jumlah konten tidak sesuai");
if (levels.some((l) => l.questions.length !== 10 || !l.textAr || !l.textId))
  throw new Error("Level tidak lengkap");
console.table(summary.map((x) => ({ ...x, words: x.words.join(", ") })));
console.log(
  "PASS: 30 materi utama, 300 pertanyaan. Pemeriksaan ini bersifat struktural; telaah bahasa dan pedagogis tetap memerlukan guru.",
);
