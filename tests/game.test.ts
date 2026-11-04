import { test } from "node:test";
import assert from "node:assert/strict";
import {
  levels,
  initialSave,
  starsFor,
  unlocked,
  bestAttempt,
  totals,
  finish,
  rubricPoints,
  parseSave,
} from "../lib/game";
import type { Attempt } from "../lib/types";
function attempt(score: number, props: Partial<Attempt> = {}): Attempt {
  return {
    id: "test",
    levelId: "istima-1",
    score,
    stars: starsFor(score),
    answers: Array.from({ length: 10 }, (_, i) => ({
      questionId: `istima-1-q${i + 1}`,
      points: i < score / 10 ? 10 : 0,
      choice: 0,
    })),
    seconds: 60,
    replays: 1,
    hints: 0,
    date: "2026-11-04T00:00:00Z",
    mode: "world",
    demo: false,
    ...props,
  };
}
test("all three worlds contain ten unique complete levels and exactly 300 unique questions", () => {
  assert.equal(levels.length, 30);
  assert.equal(new Set(levels.map((l) => l.textAr)).size, 30);
  assert.equal(
    new Set(levels.flatMap((l) => l.questions.map((q) => q.id))).size,
    300,
  );
  for (const world of ["istima", "kalam", "qiraah"])
    assert.deepEqual(
      levels.filter((l) => l.world === world).map((l) => l.number),
      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    );
  for (const l of levels) {
    assert.equal(l.questions.length, 10);
    assert.ok(l.objective && l.textId && l.mission && l.reward);
    assert.equal(l.vocabulary.length, 6);
    for (const q of l.questions) {
      assert.ok(q.explanationAr && q.explanationId);
      if (l.world === "kalam") {
        assert.ok(
          q.example && q.alternatives?.length && q.criteria && q.translation,
        );
        assert.equal(q.options, undefined);
      } else {
        assert.equal(q.options?.length, 4);
        assert.equal(new Set(q.options).size, 4);
        assert.ok(
          Number.isInteger(q.answer) && q.answer! >= 0 && q.answer! < 4,
        );
      }
    }
  }
});
test("listening stories follow suggested word ranges", () => {
  for (const l of levels.filter((l) => l.world === "istima")) {
    const n = l.textAr.split(/\s+/).length;
    const range =
      l.number <= 3
        ? [50, 80]
        : l.number <= 6
          ? [70, 100]
          : l.number <= 9
            ? [90, 130]
            : [120, 150];
    assert.ok(n >= range[0] && n <= range[1], `${l.id} has ${n} words`);
  }
});
test("star boundaries and unlocking need 60 points", () => {
  assert.deepEqual(
    [0, 59, 60, 79, 80, 89, 90, 100].map(starsFor),
    [0, 0, 1, 1, 2, 2, 3, 3],
  );
  const two = levels.find((l) => l.id === "istima-2")!;
  assert.equal(unlocked(initialSave, two), false);
  assert.equal(
    unlocked({ ...initialSave, attempts: [attempt(50)] }, two),
    false,
  );
  assert.equal(
    unlocked({ ...initialSave, attempts: [attempt(60)] }, two),
    true,
  );
});
test("demo never earns currency, best scores, or unlocks", () => {
  const s = finish(
    initialSave,
    attempt(100, { demo: true, mode: "adventure" }),
  );
  assert.equal(bestAttempt(s, "istima-1"), undefined);
  assert.equal(totals(s).stars, 0);
  assert.equal(totals(s).coins, 0);
  assert.deepEqual(s.adventure, initialSave.adventure);
});
test("retry cannot decrease best score or farm rewards", () => {
  let s = finish(initialSave, attempt(90));
  s = finish(s, attempt(100));
  s = finish(s, attempt(50));
  assert.equal(totals(s).stars, 3);
  assert.equal(totals(s).coins, 60);
  assert.equal(bestAttempt(s, "istima-1")?.score, 100);
});
test("rubric weighting is 40/25/20/15", () => {
  assert.equal(
    rubricPoints({
      relevance: 100,
      vocabulary: 0,
      structure: 0,
      comprehensibility: 0,
      feedback: "",
      source: "teacher",
    }),
    4,
  );
  assert.equal(
    rubricPoints({
      relevance: 100,
      vocabulary: 100,
      structure: 100,
      comprehensibility: 100,
      feedback: "",
      source: "teacher",
    }),
    10,
  );
});
test("adventure advances only a passed genuine stage, rolling over at three skills", () => {
  let s = finish(initialSave, attempt(50, { mode: "adventure" }));
  assert.equal(s.adventure.stage, 0);
  s = finish(s, attempt(80, { mode: "adventure" }));
  assert.equal(s.adventure.stage, 1);
  s = finish(s, attempt(80, { mode: "adventure", levelId: "kalam-1" }));
  assert.equal(s.adventure.stage, 2);
  s = finish(s, attempt(80, { mode: "adventure", levelId: "qiraah-1" }));
  assert.deepEqual(s.adventure, { chapter: 2, stage: 0 });
});
test("save roundtrip and malformed backup rejection", () => {
  const s = finish(initialSave, attempt(80));
  assert.equal(JSON.stringify(parseSave(JSON.stringify(s))), JSON.stringify(s));
  assert.throws(() => parseSave("{broken"));
  assert.throws(() =>
    parseSave(JSON.stringify({ ...s, attempts: [attempt(200)] })),
  );
  assert.throws(() =>
    parseSave(JSON.stringify({ ...s, adventure: { chapter: -1, stage: 99 } })),
  );
});
