import raw from "@/data/curriculum.json";
import type { Level, Save, World, Assessment, Attempt } from "./types";
export const levels = raw as Level[];
export const worlds: {
  id: World;
  name: string;
  ar: string;
  title: string;
  description: string;
  color: string;
  emoji: string;
  companion: string;
}[] = [
  {
    id: "istima",
    name: "Istima’",
    ar: "الاستماع",
    title: "Hutan Suara",
    description: "Dengarkan cerita, ikuti suara, temukan rahasianya.",
    color: "#82D98B",
    emoji: "🐰",
    companion: "Lulu",
  },
  {
    id: "kalam",
    name: "Kalam",
    ar: "الكلام",
    title: "Kota Percakapan",
    description: "Temui teman baru dan bercerita dalam bahasa Arab.",
    color: "#FFB984",
    emoji: "🐱",
    companion: "Mimi",
  },
  {
    id: "qiraah",
    name: "Qira’ah",
    ar: "القراءة",
    title: "Kastil Cerita",
    description: "Baca petunjuk dan buka gerbang pengetahuan.",
    color: "#B99AFF",
    emoji: "🦊",
    companion: "Rafi",
  },
];
export const initialSave: Save = {
  version: 1,
  nickname: "Penjelajah",
  avatar: "🧭",
  lang: "id",
  sound: true,
  attempts: [],
  adventure: { chapter: 1, stage: 0 },
};
export const starsFor = (score: number) =>
  score >= 90 ? 3 : score >= 80 ? 2 : score >= 60 ? 1 : 0;
export function rubricPoints(a: Assessment) {
  return (
    Math.round(
      ((a.relevance * 0.4 +
        a.vocabulary * 0.25 +
        a.structure * 0.2 +
        a.comprehensibility * 0.15) /
        10) *
        10,
    ) / 10
  );
}
export function bestAttempt(save: Save, id: string) {
  return save.attempts
    .filter((a) => a.levelId === id && !a.demo)
    .sort((a, b) => b.score - a.score)[0];
}
export function unlocked(save: Save, level: Level) {
  return (
    level.number === 1 ||
    (bestAttempt(save, `${level.world}-${level.number - 1}`)?.score ?? 0) >= 60
  );
}
export function totals(save: Save) {
  const best = levels.map((l) => bestAttempt(save, l.id));
  return {
    stars: best.reduce((n, a) => n + (a?.stars ?? 0), 0),
    coins: best.reduce((n, a) => n + (a?.stars ?? 0) * 20, 0),
    completed: best.filter((a) => (a?.score ?? 0) >= 60).length,
  };
}
export function finish(save: Save, attempt: Attempt): Save {
  const next = {
    ...save,
    attempts: [...save.attempts, attempt],
    draft: undefined,
  };
  if (
    attempt.mode === "adventure" &&
    !attempt.demo &&
    attempt.score >= 60 &&
    attempt.levelId ===
      `${worlds[save.adventure.stage].id}-${save.adventure.chapter}`
  ) {
    const stage = save.adventure.stage + 1;
    next.adventure =
      stage === 3
        ? { chapter: Math.min(11, save.adventure.chapter + 1), stage: 0 }
        : { ...save.adventure, stage };
  }
  return next;
}
export const STORAGE_KEY = "lost-expedition-v1";
export function parseSave(value: string): Save {
  const s = JSON.parse(value);
  const finite = (n: unknown, min = 0, max = Infinity) =>
    typeof n === "number" && Number.isFinite(n) && n >= min && n <= max;
  const validAnswers = (answers: unknown, level: Level, complete: boolean) =>
    Array.isArray(answers) &&
    (complete ? answers.length === 10 : answers.length <= 9) &&
    answers.every((a, i) => {
      if (
        !a ||
        a.questionId !== level.questions[i]?.id ||
        !finite(a.points, 0, 10)
      )
        return false;
      if (level.world !== "kalam")
        return Number.isInteger(a.choice) && a.choice >= 0 && a.choice < 4;
      if (
        a.transcript !== undefined &&
        (typeof a.transcript !== "string" || a.transcript.length > 5000)
      )
        return false;
      if (a.assessment) {
        return (
          ["ai", "teacher"].includes(a.assessment.source) &&
          typeof a.assessment.feedback === "string" &&
          ["relevance", "vocabulary", "structure", "comprehensibility"].every(
            (k) => finite(a.assessment[k], 0, 100),
          )
        );
      }
      return true;
    });
  if (
    !s ||
    s.version !== 1 ||
    !Array.isArray(s.attempts) ||
    s.attempts.length > 5000 ||
    typeof s.nickname !== "string" ||
    !["id", "ar"].includes(s.lang) ||
    typeof s.sound !== "boolean" ||
    !s.adventure ||
    !Number.isInteger(s.adventure.chapter) ||
    s.adventure.chapter < 1 ||
    s.adventure.chapter > 11 ||
    !Number.isInteger(s.adventure.stage) ||
    s.adventure.stage < 0 ||
    s.adventure.stage > 2
  )
    throw new Error("Format progres tidak sesuai.");
  for (const a of s.attempts) {
    const level = levels.find((l) => l.id === a?.levelId);
    if (
      !level ||
      !finite(a.score, 0, 100) ||
      a.stars !== starsFor(a.score) ||
      typeof a.demo !== "boolean" ||
      !["world", "adventure"].includes(a.mode) ||
      !validAnswers(a.answers, level, true) ||
      !finite(a.seconds) ||
      !finite(a.replays) ||
      !finite(a.hints) ||
      typeof a.id !== "string" ||
      typeof a.date !== "string" ||
      Number.isNaN(Date.parse(a.date))
    )
      throw new Error("Data percobaan tidak valid.");
  }
  if (s.draft) {
    const d = s.draft;
    const level = levels.find((l) => l.id === d.levelId);
    if (
      !level ||
      !validAnswers(d.answers, level, false) ||
      !["study", "quiz"].includes(d.phase) ||
      typeof d.heard !== "boolean" ||
      typeof d.demo !== "boolean" ||
      !["world", "adventure"].includes(d.mode) ||
      !finite(d.seconds) ||
      !finite(d.replays) ||
      !finite(d.hints) ||
      !Number.isInteger(d.chapter) ||
      d.chapter < 1 ||
      d.chapter > 10
    )
      s.draft = undefined;
  }
  if (typeof s.avatar !== "string" || s.avatar.length > 10)
    throw new Error("Avatar tidak valid.");
  return { ...initialSave, ...s, nickname: s.nickname.slice(0, 24) } as Save;
}
