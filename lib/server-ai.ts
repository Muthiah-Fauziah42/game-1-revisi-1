import "server-only";
import { timingSafeEqual } from "node:crypto";
const buckets = new Map<string, { count: number; reset: number }>();
export function guard(request: Request): Response | null {
  if (!process.env.OPENAI_API_KEY || !process.env.AI_ACCESS_TOKEN)
    return Response.json(
      {
        error:
          "Layanan AI belum diaktifkan pengelola. Gunakan suara perangkat atau penilaian bersama guru.",
      },
      { status: 503 },
    );
  const expected = Buffer.from(process.env.AI_ACCESS_TOKEN);
  const actual = Buffer.from(request.headers.get("X-AI-Access") || "");
  if (actual.length !== expected.length || !timingSafeEqual(actual, expected))
    return Response.json(
      {
        error:
          "Token akses layanan belum sesuai. Minta guru memeriksa Pengaturan.",
      },
      { status: 403 },
    );
  const origin = request.headers.get("origin");
  if (origin && new URL(origin).host !== new URL(request.url).host)
    return Response.json(
      { error: "Asal permintaan tidak diizinkan." },
      { status: 403 },
    );
  const ip =
    request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "local";
  const now = Date.now();
  const old = buckets.get(ip);
  const entry = old && old.reset > now ? old : { count: 0, reset: now + 60000 };
  if (entry.count >= 15)
    return Response.json(
      { error: "Terlalu banyak permintaan. Tunggu satu menit lalu coba lagi." },
      { status: 429, headers: { "Retry-After": "60" } },
    );
  entry.count++;
  buckets.set(ip, entry);
  if (buckets.size > 10000)
    for (const [k, v] of buckets) if (v.reset <= now) buckets.delete(k);
  return null;
}
export async function callAI(
  path: string,
  body: BodyInit,
  headers: Record<string, string> = {},
) {
  const response = await fetch(`https://api.openai.com/v1/${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      ...headers,
    },
    body,
    signal: AbortSignal.timeout(45000),
  });
  if (!response.ok)
    throw new Error(
      "Layanan AI belum dapat memproses permintaan. Coba lagi atau gunakan penilaian guru.",
    );
  return response;
}
export async function jsonAI(system: string, data: unknown) {
  const r = await callAI(
    "chat/completions",
    JSON.stringify({
      model: process.env.OPENAI_TEXT_MODEL || "gpt-4.1-mini",
      temperature: 0.25,
      response_format: { type: "json_object" },
      messages: [
        { role: "system", content: system },
        { role: "user", content: JSON.stringify(data) },
      ],
      max_completion_tokens: 1200,
    }),
    { "Content-Type": "application/json" },
  );
  const result = await r.json();
  const content = result.choices?.[0]?.message?.content;
  if (!content) throw new Error("Jawaban AI kosong. Coba ulangi.");
  return JSON.parse(content);
}
export async function bodyJSON(request: Request) {
  const text = await request.text();
  if (text.length > 12000) throw new Error("Permintaan terlalu besar.");
  return JSON.parse(text);
}
export function apiError(e: unknown) {
  return Response.json(
    { error: e instanceof Error ? e.message : "Layanan belum tersedia." },
    { status: 502 },
  );
}
