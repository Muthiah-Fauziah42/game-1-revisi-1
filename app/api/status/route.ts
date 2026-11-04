export function GET() {
  return Response.json(
    {
      enabled: Boolean(
        process.env.OPENAI_API_KEY && process.env.AI_ACCESS_TOKEN,
      ),
    },
    { headers: { "Cache-Control": "no-store" } },
  );
}
