import { test } from "node:test";
import assert from "node:assert/strict";
import { POST as speech } from "../app/api/speech/route";
import { POST as evaluate } from "../app/api/evaluate/route";
import { POST as transcribe } from "../app/api/transcribe/route";
import { POST as tutor } from "../app/api/tutor/route";
const req = (path: string, body: unknown = {}, token = "") =>
  new Request(`http://localhost/api/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-AI-Access": token },
    body: JSON.stringify(body),
  });
test("paid endpoints require configuration, authenticate access and reject invalid curriculum IDs without upstream requests", async () => {
  const oldKey = process.env.OPENAI_API_KEY;
  const oldToken = process.env.AI_ACCESS_TOKEN;
  try {
    delete process.env.OPENAI_API_KEY;
    delete process.env.AI_ACCESS_TOKEN;
    for (const [path, fn] of [
      ["speech", speech],
      ["evaluate", evaluate],
      ["transcribe", transcribe],
      ["tutor", tutor],
    ] as const)
      assert.equal((await fn(req(path))).status, 503);
    process.env.OPENAI_API_KEY = "test-never-sent";
    process.env.AI_ACCESS_TOKEN = "test-access";
    assert.equal((await speech(req("speech", {}, "wrong"))).status, 403);
    assert.equal(
      (await speech(req("speech", { id: "not-a-level" }, "test-access")))
        .status,
      404,
    );
    assert.equal(
      (
        await evaluate(
          req(
            "evaluate",
            { levelId: "kalam-1", questionId: "wrong", transcript: "مرحبا" },
            "test-access",
          ),
        )
      ).status,
      400,
    );
    assert.equal(
      (
        await tutor(
          req("tutor", { levelId: "wrong", score: 50 }, "test-access"),
        )
      ).status,
      400,
    );
  } finally {
    if (oldKey === undefined) delete process.env.OPENAI_API_KEY;
    else process.env.OPENAI_API_KEY = oldKey;
    if (oldToken === undefined) delete process.env.AI_ACCESS_TOKEN;
    else process.env.AI_ACCESS_TOKEN = oldToken;
  }
});
