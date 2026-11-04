import { levels } from "@/lib/game";
import { guard, callAI, bodyJSON, apiError } from "@/lib/server-ai";
export const runtime = "nodejs";
export const maxDuration = 60;
export async function POST(request: Request) {
  const denied = guard(request);
  if (denied) return denied;
  try {
    const { id } = await bodyJSON(request);
    if (typeof id !== "string")
      return Response.json({ error: "ID audio tidak valid." }, { status: 400 });
    const canonical = id.replace(/-relisten$/, "");
    let text = levels.find((l) => l.id === canonical)?.textAr;
    if (!text)
      text = levels
        .flatMap((l) => l.questions)
        .find((q) => q.id === canonical)?.ar;
    if (!text)
      return Response.json(
        { error: "Materi audio tidak ditemukan." },
        { status: 404 },
      );
    const r = await callAI(
      "audio/speech",
      JSON.stringify({
        model: process.env.OPENAI_TTS_MODEL || "gpt-4o-mini-tts",
        voice: "alloy",
        input: text,
        response_format: "mp3",
        speed: 0.85,
      }),
      { "Content-Type": "application/json" },
    );
    return new Response(await r.arrayBuffer(), {
      headers: {
        "Content-Type": "audio/mpeg",
        "Cache-Control": "private, max-age=86400",
      },
    });
  } catch (e) {
    return apiError(e);
  }
}
