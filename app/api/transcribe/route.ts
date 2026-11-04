import { guard, callAI, apiError } from "@/lib/server-ai";
export const runtime = "nodejs";
export const maxDuration = 60;
export async function POST(request: Request) {
  const denied = guard(request);
  if (denied) return denied;
  try {
    if (Number(request.headers.get("content-length") || 0) > 4000000)
      return Response.json(
        { error: "Rekaman maksimal 4 MB." },
        { status: 413 },
      );
    const incoming = await request.formData();
    const file = incoming.get("file");
    if (
      !(file instanceof File) ||
      file.size < 100 ||
      file.size > 4000000 ||
      ![
        "audio/webm",
        "audio/mp4",
        "audio/mpeg",
        "audio/wav",
        "audio/ogg",
      ].includes(file.type.split(";")[0])
    )
      return Response.json(
        { error: "Format atau ukuran rekaman tidak didukung. Maksimal 4 MB." },
        { status: 400 },
      );
    const form = new FormData();
    form.append("file", file);
    form.append(
      "model",
      process.env.OPENAI_TRANSCRIBE_MODEL || "gpt-4o-mini-transcribe",
    );
    form.append("language", "ar");
    const r = await callAI("audio/transcriptions", form);
    const data = await r.json();
    if (typeof data.text !== "string")
      throw new Error("Suara belum dapat dikenali. Coba rekam ulang.");
    return Response.json(
      { text: data.text.slice(0, 1500) },
      { headers: { "Cache-Control": "no-store" } },
    );
  } catch (e) {
    return apiError(e);
  }
}
