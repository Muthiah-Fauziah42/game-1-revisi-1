/** Optional build-time TTS: creates teacher-reviewable MP3s; never exposes API keys to visitors. */
import { readFile, mkdir, writeFile, stat } from "node:fs/promises";
const key = process.env.OPENAI_API_KEY;
if (!key)
  throw new Error(
    "Atur OPENAI_API_KEY di lingkungan terminal; jangan masukkan ke kode.",
  );
const levels = JSON.parse(
  await readFile(new URL("../data/curriculum.json", import.meta.url), "utf8"),
);
const items = levels
  .filter((l) => l.world !== "qiraah")
  .flatMap((l) => [
    { id: l.id, text: l.textAr },
    ...l.questions.map((q) => ({ id: q.id, text: q.ar })),
  ]);
await mkdir(new URL("../public/audio/", import.meta.url), { recursive: true });
let count = 0;
for (const item of items) {
  const output = new URL(`../public/audio/${item.id}.mp3`, import.meta.url);
  try {
    if ((await stat(output)).size > 1000) {
      count++;
      continue;
    }
  } catch {}
  const r = await fetch("https://api.openai.com/v1/audio/speech", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: process.env.OPENAI_TTS_MODEL || "gpt-4o-mini-tts",
      voice: "alloy",
      input: item.text,
      speed: 0.85,
      response_format: "mp3",
    }),
    signal: AbortSignal.timeout(60000),
  });
  if (!r.ok)
    throw new Error(
      `Gagal menghasilkan ${item.id} (HTTP ${r.status}); jalankan ulang untuk melanjutkan.`,
    );
  await writeFile(output, Buffer.from(await r.arrayBuffer()));
  count++;
  console.log(`${count}/${items.length} ${item.id}`);
}
