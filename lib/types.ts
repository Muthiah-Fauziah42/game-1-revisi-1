export type World = "istima" | "kalam" | "qiraah";
export interface Question {
  id: string;
  ar: string;
  options?: string[];
  answer?: number;
  translation?: string;
  example?: string;
  alternatives?: string[];
  criteria?: string;
  explanationAr: string;
  explanationId: string;
  category: string;
}
export interface Level {
  id: string;
  world: World;
  number: number;
  title: string;
  titleAr: string;
  scene: string;
  objective: string;
  mission: string;
  character: string;
  textAr: string;
  textId: string;
  vocabulary: { ar: string; id: string }[];
  questions: Question[];
  reward: string;
  difficulty: string;
}
export interface Assessment {
  relevance: number;
  vocabulary: number;
  structure: number;
  comprehensibility: number;
  feedback: string;
  correction?: string;
  source: "ai" | "teacher";
}
export interface Answer {
  questionId: string;
  choice?: number;
  transcript?: string;
  assessment?: Assessment;
  points: number;
  exampleViewed?: boolean;
}
export interface Attempt {
  id: string;
  levelId: string;
  score: number;
  stars: number;
  answers: Answer[];
  seconds: number;
  replays: number;
  hints: number;
  date: string;
  mode: "world" | "adventure";
  demo: boolean;
}
export interface Draft {
  levelId: string;
  answers: Answer[];
  phase: "study" | "quiz";
  heard: boolean;
  seconds: number;
  replays: number;
  hints: number;
  mode: "world" | "adventure";
  chapter: number;
  demo: boolean;
}
export interface Save {
  version: 1;
  nickname: string;
  avatar: string;
  lang: "id" | "ar";
  sound: boolean;
  attempts: Attempt[];
  draft?: Draft;
  adventure: { chapter: number; stage: number };
}
