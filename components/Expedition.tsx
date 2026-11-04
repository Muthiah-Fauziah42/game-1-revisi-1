"use client";
import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight,
  ArrowLeft,
  Map,
  Compass,
  Star,
  Coins,
  Settings,
  Home,
  ChartNoAxesColumnIncreasing,
  Lock,
  Check,
  ChevronRight,
  Volume2,
  VolumeX,
  BookOpen,
  Headphones,
  Mic,
  Trophy,
  Download,
  Upload,
  X,
  Flag,
  Lightbulb,
  RotateCcw,
  ShieldCheck,
} from "lucide-react";
import {
  levels,
  worlds,
  initialSave,
  STORAGE_KEY,
  parseSave,
  bestAttempt,
  unlocked,
  totals,
  starsFor,
  finish,
} from "@/lib/game";
import type { Save, World, Level, Draft, Answer, Attempt } from "@/lib/types";
import Tutor from "./Tutor";
import Scenery from "./Scenery";
import AudioPlayer from "./AudioPlayer";
import Speaking from "./Speaking";
type View = "home" | "map" | "play" | "result" | "progress" | "adventure";
const arNav = {
  home: "الرَّئِيسِيَّةُ",
  map: "الْعَوَالِمُ",
  progress: "تَقَدُّمِي",
  settings: "الْإِعْدَادَاتُ",
};
const adventureChapters = [
  "Gerbang pertemanan",
  "Bekal sang penjelajah",
  "Ruang penuh warna",
  "Keluarga penjaga peta",
  "Jejak hewan hutan",
  "Hari persiapan",
  "Petunjuk di desa",
  "Jalan menuju menara",
  "Rahasia pasar",
  "Harta pengetahuan",
];
function Stars({ count = 0 }: { count?: number }) {
  return (
    <span className="stars" aria-label={`${count} dari 3 bintang`}>
      {[0, 1, 2].map((i) => (
        <Star
          key={i}
          size={17}
          fill={i < count ? "#f4bd37" : "transparent"}
          color={i < count ? "#e6a824" : "#bdc8d4"}
        />
      ))}
    </span>
  );
}
export default function Expedition() {
  const [save, setSave] = useState<Save>(initialSave);
  const [loaded, setLoaded] = useState(false);
  const [storageError, setStorageError] = useState("");
  const [view, setView] = useState<View>("home");
  const [world, setWorld] = useState<World>("istima");
  const [draft, setDraft] = useState<Draft | null>(null);
  const [result, setResult] = useState<Attempt | null>(null);
  const [selected, setSelected] = useState<number | null>(null);
  const [settings, setSettings] = useState(false);
  const [profile, setProfile] = useState(false);
  const [hint, setHint] = useState(false);
  const [reset, setReset] = useState(false);
  const [audioToken, setAudioToken] = useState("");
  const [services, setServices] = useState("");
  const modalRef = useRef<HTMLElement>(null);
  const importInput = useRef<HTMLInputElement>(null);
  const answerGuard = useRef(false);
  const preserveOriginal = useRef(false);
  const originalSave = useRef("");
  const saveRef = useRef(save);
  saveRef.current = save;
  const draftRef = useRef(draft);
  draftRef.current = draft;
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        originalSave.current = stored;
        setSave(parseSave(stored));
      }
    } catch {
      preserveOriginal.current = true;
      setStorageError(
        "Progres tersimpan belum dapat dibaca. Unduh cadangannya melalui Pengaturan sebelum mengatur ulang.",
      );
    }
    try {
      setAudioToken(sessionStorage.getItem("expedition-ai-token") || "");
    } catch {}
    setLoaded(true);
  }, []);
  useEffect(() => {
    if (!loaded || preserveOriginal.current) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(save));
    } catch {
      setStorageError(
        "Penyimpanan perangkat tidak tersedia atau penuh. Unduh progres agar tidak hilang.",
      );
    }
  }, [save, loaded]);
  useEffect(() => {
    if (!draft || view !== "play") return;
    const timer = setInterval(
      () => setDraft((d) => (d ? { ...d, seconds: d.seconds + 1 } : d)),
      1000,
    );
    return () => clearInterval(timer);
  }, [!!draft, view]);
  useEffect(() => {
    if (loaded && draft) setSave((s) => ({ ...s, draft }));
  }, [draft, loaded]);
  useEffect(() => {
    function flush() {
      if (draftRef.current && !preserveOriginal.current) {
        try {
          localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify({ ...saveRef.current, draft: draftRef.current }),
          );
        } catch {}
      }
    }
    window.addEventListener("pagehide", flush);
    return () => window.removeEventListener("pagehide", flush);
  }, []);
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
    setSelected(null);
    setHint(false);
    answerGuard.current = false;
  }, [view, draft?.levelId, draft?.answers.length]);
  useEffect(() => {
    if (settings) {
      fetch("/api/status")
        .then((r) => r.json())
        .then((d) =>
          setServices(
            d.enabled
              ? "Server AI telah dikonfigurasi. Token akses tetap diperlukan."
              : "Server AI belum dikonfigurasi. Rekaman guru dan suara Arab perangkat tetap dapat digunakan.",
          ),
        )
        .catch(() => setServices("Status server belum dapat diperiksa."));
    }
  }, [settings]);
  useEffect(() => {
    if (!settings && !profile) return;
    const previous = document.activeElement as HTMLElement | null;
    modalRef.current?.querySelector<HTMLElement>("button")?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setSettings(false);
        setProfile(false);
      }
      if (e.key === "Tab") {
        const focusable = Array.from(
          modalRef.current?.querySelectorAll<HTMLElement>(
            "button:not(:disabled),input:not([hidden]),select,summary",
          ) || [],
        ).filter((el) => el.getClientRects().length);
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last?.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first?.focus();
        }
      }
    };
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("keydown", onKey);
      previous?.focus();
    };
  }, [settings, profile]);
  const t = (key: keyof typeof arNav, other: string) =>
    save.lang === "ar" ? arNav[key] : other;
  const total = totals(save);
  const active = levels.find((l) => l.id === draft?.levelId);
  const current = active?.questions[draft?.answers.length ?? 0];
  const currentWorld = worlds.find((w) => w.id === world)!;
  function navigate(v: View) {
    setView(v);
    if (v !== "play") window.speechSynthesis?.cancel();
  }
  function openWorld(w: World) {
    setWorld(w);
    navigate("map");
  }
  function start(
    level: Level,
    mode: "world" | "adventure" = "world",
    demo = false,
  ) {
    if (mode === "world" && !demo && !unlocked(save, level)) return;
    const d: Draft = {
      levelId: level.id,
      answers: [],
      phase: "study",
      heard: false,
      seconds: 0,
      replays: 0,
      hints: 0,
      mode,
      chapter: mode === "adventure" ? level.number : save.adventure.chapter,
      demo,
    };
    setDraft(d);
    setSave((s) => ({ ...s, draft: d }));
    setWorld(level.world);
    navigate("play");
  }
  function resume() {
    if (save.draft) {
      setDraft(save.draft);
      setWorld(levels.find((l) => l.id === save.draft?.levelId)!.world);
      navigate("play");
    }
  }
  function bumpReplay() {
    setDraft((d) => (d ? { ...d, replays: d.replays + 1 } : d));
  }
  function submit(answer: Answer) {
    if (!draft || !active || answerGuard.current) return;
    answerGuard.current = true;
    const answers = [...draft.answers, answer];
    if (answers.length < 10) {
      setDraft({ ...draft, answers });
      setSelected(null);
      return;
    }
    const score = Math.round(answers.reduce((n, a) => n + a.points, 0));
    const attempt: Attempt = {
      id: crypto.randomUUID(),
      levelId: active.id,
      score,
      stars: starsFor(score),
      answers,
      seconds: draft.seconds,
      replays: draft.replays,
      hints: draft.hints,
      date: new Date().toISOString(),
      mode: draft.mode,
      demo: draft.demo,
    };
    setSave((s) => finish(s, attempt));
    setResult(attempt);
    setDraft(null);
    navigate("result");
  }
  function startAdventure() {
    const chapter = save.adventure.chapter;
    if (chapter > 10) return;
    const w = worlds[save.adventure.stage].id;
    start(
      levels.find((l) => l.world === w && l.number === chapter)!,
      "adventure",
    );
  }
  function backup() {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(
      new Blob(
        [
          preserveOriginal.current
            ? originalSave.current
            : JSON.stringify(save, null, 2),
        ],
        { type: "application/json" },
      ),
    );
    a.download = "lost-expedition-progres.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }
  function exportCSV() {
    const lines = [
      "level,nilai,bintang,detik,percobaan_audio,petunjuk,mode,tanggal",
      ...save.attempts.map((a) =>
        [
          a.levelId,
          a.score,
          a.stars,
          a.seconds,
          a.replays,
          a.hints,
          a.demo ? "demo" : a.mode,
          a.date,
        ].join(","),
      ),
    ];
    const a = document.createElement("a");
    a.href = URL.createObjectURL(
      new Blob(["\uFEFF" + lines.join("\n")], {
        type: "text/csv;charset=utf-8",
      }),
    );
    a.download = "lost-expedition-laporan.csv";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }
  async function restore(file?: File) {
    if (!file) return;
    try {
      if (file.size > 5000000)
        throw new Error("Berkas terlalu besar. Maksimal 5 MB.");
      const parsed = parseSave(await file.text());
      preserveOriginal.current = false;
      setSave(parsed);
      setDraft(null);
      setStorageError("");
      setServices("Cadangan progres berhasil dipulihkan.");
      navigate("home");
    } catch (e) {
      setServices(e instanceof Error ? e.message : "Cadangan tidak valid.");
    }
    if (importInput.current) importInput.current.value = "";
  }
  const allReal = save.attempts.filter((a) => !a.demo);
  const resultLevel = levels.find((l) => l.id === result?.levelId);
  const doneWorld = worlds.filter((w) =>
    levels
      .filter((l) => l.world === w.id)
      .every((l) => (bestAttempt(save, l.id)?.score ?? 0) >= 60),
  );
  return (
    <div className="app-shell">
      <header className="site-header">
        <button
          className="brand"
          onClick={() => navigate("home")}
          aria-label="Kembali ke beranda"
        >
          <span className="brand-icon">
            <Compass size={28} />
          </span>
          <span>
            <b>
              THE LOST
              <br />
              <span>EXPEDITION</span>
            </b>
            <small>رِحْلَةُ الْمَفْقُودِ</small>
          </span>
        </button>
        <nav className="desktop-nav">
          <button
            className={view === "home" ? "nav-active" : ""}
            onClick={() => navigate("home")}
          >
            {t("home", "Beranda")}
          </button>
          <button
            className={["map", "play"].includes(view) ? "nav-active" : ""}
            onClick={() => openWorld(world)}
          >
            {t("map", "Dunia Petualangan")}
          </button>
          <button
            className={view === "progress" ? "nav-active" : ""}
            onClick={() => navigate("progress")}
          >
            {t("progress", "Progresku")}
          </button>
        </nav>
        <div className="header-right">
          <span className="currency">
            <Star size={17} fill="#FFD95A" color="#d8a22a" />
            {total.stars}
          </span>
          <span className="currency coin">
            <Coins size={18} />
            {total.coins}
          </span>
          <button
            className="icon-btn settings-trigger"
            aria-label="Pengaturan"
            onClick={() => setSettings(true)}
          >
            <Settings size={21} />
          </button>
          <button
            className="avatar"
            onClick={() => setProfile(true)}
            aria-label="Ubah profil pemain"
          >
            {save.avatar}
          </button>
        </div>
      </header>
      {storageError && (
        <div className="storage-alert" role="alert">
          {storageError}
        </div>
      )}
      <main id="main">
        <AnimatePresence mode="wait">
          <motion.div
            key={view}
            initial={false}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            {view === "home" && (
              <>
                <section className="hero">
                  <div className="hero-copy">
                    <span className="eyebrow">
                      <span /> BELAJAR BAHASA ARAB, SAMBIL BERPETUALANG
                    </span>
                    <h1>
                      Petualangan besar.
                      <br />
                      <em>Dimulai dari kamu.</em>
                    </h1>
                    <p>
                      Di balik hutan, kota, dan kastil, ada rahasia yang
                      menunggumu. Siap menemukannya dengan Bahasa Arab?
                    </p>
                    <div className="hero-actions">
                      <button
                        className="btn primary large"
                        disabled={!loaded}
                        onClick={
                          save.draft ? resume : () => openWorld("istima")
                        }
                      >
                        <Compass size={20} />
                        {save.draft
                          ? "Lanjutkan Petualangan"
                          : "Mulai Petualangan"}
                        <ArrowRight size={20} />
                      </button>
                      <span className="age-note">
                        Untuk penjelajah
                        <br />
                        <b>usia 7–12 tahun</b>
                      </span>
                    </div>
                    <div className="hero-proof">
                      <span>
                        <Check size={15} /> 3 dunia seru
                      </span>
                      <span>
                        <Check size={15} /> 30 misi belajar
                      </span>
                      <span>
                        <Check size={15} /> 300 tantangan
                      </span>
                    </div>
                  </div>
                  <div className="hero-visual">
                    <div className="floating-note">
                      <span>🦉</span>
                      <div>
                        <b>Ahlan, {save.nickname}!</b>
                        <small>Mari temukan harta pengetahuan.</small>
                      </div>
                    </div>
                    <Scenery />
                    <span className="map-tag map-tag-one">🌿 Dengarkan</span>
                    <span className="map-tag map-tag-two">💬 Bicarakan</span>
                    <span className="map-tag map-tag-three">📖 Temukan</span>
                    <div className="hero-stamp">
                      <Star fill="#FFD95A" size={18} /> SETIAP LANGKAH, MAKIN
                      HEBAT
                    </div>
                  </div>
                </section>
                <section className="welcome-strip">
                  <div className="welcome-character">{save.avatar}</div>
                  <div>
                    <strong>Senang melihatmu, {save.nickname}!</strong>
                    <p>
                      {total.completed === 0
                        ? "Petualangan pertamamu menanti. Pilih sebuah dunia di bawah."
                        : `${total.completed} misi sudah kamu taklukkan. Ayo lanjutkan penjelajahan!`}
                    </p>
                  </div>
                  <div className="mini-progress">
                    <span>
                      Peta petualangan <b>{total.completed}/30</b>
                    </span>
                    <div className="progress-track">
                      <i
                        style={{ width: `${(total.completed / 30) * 100}%` }}
                      />
                    </div>
                  </div>
                  <button
                    className="text-button"
                    onClick={() => navigate("progress")}
                  >
                    Lihat progres <ChevronRight size={16} />
                  </button>
                </section>
                <section className="world-section">
                  <div className="section-heading">
                    <div>
                      <span className="eyebrow">
                        SATU PETUALANGAN, TIGA KEMAMPUAN
                      </span>
                      <h2>
                        Pilih dunia pertamamu <span>✦</span>
                      </h2>
                    </div>
                    <p>
                      Setiap dunia punya cerita.
                      <br />
                      Setiap misi membuatmu bisa.
                    </p>
                  </div>
                  <div className="world-grid">
                    {worlds.map((w, i) => {
                      const passed = levels.filter(
                        (l) =>
                          l.world === w.id &&
                          (bestAttempt(save, l.id)?.score ?? 0) >= 60,
                      ).length;
                      return (
                        <button
                          key={w.id}
                          className={`world-card world-${w.id}`}
                          onClick={() => openWorld(w.id)}
                        >
                          <div className="world-picture">
                            <Scenery
                              type={
                                i === 0 ? "forest" : i === 1 ? "town" : "castle"
                              }
                            />
                            <span className="world-index">DUNIA 0{i + 1}</span>
                            <span className="world-character">{w.emoji}</span>
                          </div>
                          <div className="world-body">
                            <div className="world-title-row">
                              <span className="world-skill">
                                {i === 0 ? (
                                  <Headphones size={15} />
                                ) : i === 1 ? (
                                  <Mic size={15} />
                                ) : (
                                  <BookOpen size={15} />
                                )}{" "}
                                {w.name} ·{" "}
                                {i === 0
                                  ? "Menyimak"
                                  : i === 1
                                    ? "Berbicara"
                                    : "Membaca"}
                              </span>
                              <span
                                className="arabic world-ar"
                                lang="ar"
                                dir="rtl"
                              >
                                {w.ar}
                              </span>
                            </div>
                            <h3>{w.title}</h3>
                            <p>{w.description}</p>
                            <div className="world-card-bottom">
                              <span>
                                <Flag size={14} /> {passed}/10 misi selesai
                              </span>
                              <span className="round-arrow">
                                <ArrowRight size={18} />
                              </span>
                            </div>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </section>
                <section className="adventure-banner">
                  <div className="treasure">🗺️</div>
                  <div>
                    <span className="eyebrow">MODE PETUALANGAN TERPADU</span>
                    <h2>Satu tim. Satu pulau. Banyak rahasia.</h2>
                    <p>
                      Gabungkan menyimak, berbicara, dan membaca untuk menemukan
                      harta yang hilang.
                    </p>
                  </div>
                  <button
                    className="btn navy"
                    onClick={() => navigate("adventure")}
                  >
                    Jelajahi pulau <ArrowRight size={18} />
                  </button>
                </section>
                <div className="learning-note">
                  <ShieldCheck size={18} />
                  <span>
                    Belajar sesuai langkahmu · Tanpa batas waktu soal · Progres
                    tersimpan di perangkat ini
                  </span>
                </div>
              </>
            )}
            {view === "map" && (
              <section className={`map-page theme-${world}`}>
                <button
                  className="text-button back"
                  onClick={() => navigate("home")}
                >
                  <ArrowLeft size={16} /> Kembali ke beranda
                </button>
                <div className="map-intro">
                  <span className="companion-avatar">{currentWorld.emoji}</span>
                  <div>
                    <span className="eyebrow">
                      DUNIA {worlds.findIndex((w) => w.id === world) + 1} ·{" "}
                      {currentWorld.name.toUpperCase()}
                    </span>
                    <h1>{currentWorld.title}</h1>
                    <p>
                      Aku {currentWorld.companion}, teman perjalananmu! Raih
                      nilai 60 untuk membuka misi berikutnya.
                    </p>
                  </div>
                  <span className="arabic large-ar" dir="rtl" lang="ar">
                    {currentWorld.ar}
                  </span>
                </div>
                <div className="world-tabs">
                  {worlds.map((w) => (
                    <button
                      key={w.id}
                      className={world === w.id ? "active" : ""}
                      onClick={() => setWorld(w.id)}
                    >
                      {w.emoji} {w.title}
                    </button>
                  ))}
                </div>
                <div className="map-layout">
                  <div className="level-path">
                    {levels
                      .filter((l) => l.world === world)
                      .map((l) => {
                        const best = bestAttempt(save, l.id);
                        const available = unlocked(save, l);
                        const inProgress = save.draft?.levelId === l.id;
                        return (
                          <div
                            key={l.id}
                            className={`level-stop ${available ? "" : "locked"} ${best?.stars ? "passed" : ""}`}
                          >
                            <button
                              className="level-number"
                              disabled={!available}
                              onClick={() => (inProgress ? resume() : start(l))}
                              aria-label={`Level ${l.number}: ${l.title}${!available ? ", terkunci" : ""}`}
                            >
                              {available ? (
                                best?.stars ? (
                                  <Check />
                                ) : (
                                  l.number
                                )
                              ) : (
                                <Lock size={20} />
                              )}
                            </button>
                            <button
                              className="level-info"
                              disabled={!available}
                              onClick={() => (inProgress ? resume() : start(l))}
                            >
                              <span className="level-caption">
                                MISI {String(l.number).padStart(2, "0")} ·{" "}
                                {l.difficulty}
                              </span>
                              <strong>{l.title}</strong>
                              <span className="arabic" dir="rtl" lang="ar">
                                {l.titleAr}
                              </span>
                              <div className="level-status">
                                <Stars count={best?.stars} />
                                <small>
                                  {inProgress
                                    ? "Sedang dimainkan"
                                    : best?.stars
                                      ? "Selesai"
                                      : available
                                        ? "Siap dijelajahi"
                                        : "Selesaikan misi sebelumnya"}
                                </small>
                              </div>
                            </button>
                          </div>
                        );
                      })}
                    <span className="path-treasure">🏆</span>
                  </div>
                  <aside className="map-aside">
                    <Scenery
                      type={
                        world === "istima"
                          ? "forest"
                          : world === "kalam"
                            ? "town"
                            : "castle"
                      }
                    />
                    <div className="aside-content">
                      <span className="companion-small">🦉</span>
                      <h3>Selangkah demi selangkah.</h3>
                      <p>
                        Setiap misi berisi materi baru dan 10 tantangan. Tidak
                        perlu terburu-buru; kamu selalu boleh mencoba lagi.
                      </p>
                      <div className="legend">
                        <span>
                          <i className="available-dot" /> Tersedia
                        </span>
                        <span>
                          <i className="complete-dot" /> Selesai
                        </span>
                        <span>
                          <Lock size={12} /> Terkunci
                        </span>
                      </div>
                      <p className="muted">
                        Ingin memeriksa materi dahulu? Mode demo membuka pilihan
                        semua level. Hasil demo tidak menghasilkan bintang atau
                        membuka progres.
                      </p>
                      <button
                        className="btn secondary"
                        onClick={() => {
                          setProfile(false);
                          setSettings(true);
                        }}
                      >
                        Buka mode demo <ArrowRight size={16} />
                      </button>
                    </div>
                  </aside>
                </div>
              </section>
            )}
            {view === "adventure" && (
              <section className="adventure-page">
                <button
                  className="text-button back"
                  onClick={() => navigate("home")}
                >
                  <ArrowLeft size={16} /> Beranda
                </button>
                <div className="page-heading">
                  <span className="eyebrow">PETUALANGAN TERPADU</span>
                  <h1>Pulau Harta Pengetahuan</h1>
                  <p>
                    Sepuluh bab, satu perjalanan. Dengarkan petunjuk Lulu, ajak
                    Mimi berbicara, lalu baca bersama Rafi.
                  </p>
                </div>
                <div className="adventure-hero">
                  <Scenery />
                  <div className="adventure-panel">
                    <span className="eyebrow">
                      {save.adventure.chapter > 10
                        ? "SELURUH BAB SELESAI"
                        : `BAB ${save.adventure.chapter} DARI 10`}
                    </span>
                    <h2>
                      {save.adventure.chapter > 10
                        ? "Kamu penjelajah sejati!"
                        : adventureChapters[save.adventure.chapter - 1]}
                    </h2>
                    <p>
                      {save.adventure.chapter > 10
                        ? "Harta terbesar adalah ilmu yang kamu bagikan. Ulangi dunia pilihanmu untuk memperkuat kemampuan."
                        : "Burung hantu kehilangan gulungan pengetahuan. Setiap bab menghubungkan tiga kemampuan untuk mengumpulkan kembali lembarannya."}
                    </p>
                    <ol className="adventure-steps">
                      {worlds.map((w, i) => (
                        <li
                          key={w.id}
                          className={
                            i === save.adventure.stage ? "current" : ""
                          }
                        >
                          <span>
                            {i < save.adventure.stage ? (
                              <Check size={16} />
                            ) : (
                              w.emoji
                            )}
                          </span>
                          <div>
                            <b>{w.name}</b>
                            <small>
                              {i === 0
                                ? "Dengarkan petunjuk perjalanan"
                                : i === 1
                                  ? "Berbicaralah dengan penduduk"
                                  : "Baca catatan pengetahuan"}
                            </small>
                          </div>
                        </li>
                      ))}
                    </ol>
                    {save.adventure.chapter <= 10 && (
                      <button
                        className="btn primary"
                        onClick={
                          save.draft?.mode === "adventure"
                            ? resume
                            : startAdventure
                        }
                      >
                        Lanjutkan bab ini <ArrowRight size={18} />
                      </button>
                    )}
                  </div>
                </div>
                <div className="chapter-grid">
                  {adventureChapters.map((c, i) => (
                    <div
                      key={c}
                      className={
                        i + 1 < save.adventure.chapter
                          ? "chapter done"
                          : i + 1 === save.adventure.chapter
                            ? "chapter current"
                            : "chapter"
                      }
                    >
                      <span>
                        {i + 1 < save.adventure.chapter ? "✓" : i + 1}
                      </span>
                      <b>{c}</b>
                      <small>
                        {i + 1 < save.adventure.chapter
                          ? "Lembar ditemukan"
                          : i + 1 === save.adventure.chapter
                            ? "Misi aktif"
                            : "Belum terbuka"}
                      </small>
                    </div>
                  ))}
                </div>
              </section>
            )}
            {view === "play" && active && draft && current && (
              <section className="play-page">
                <div className="play-top">
                  <button
                    className="text-button"
                    onClick={() =>
                      navigate(draft.mode === "adventure" ? "adventure" : "map")
                    }
                  >
                    <ArrowLeft size={17} /> Simpan & kembali
                  </button>
                  <span className="pill">
                    {draft.demo
                      ? "MODE DEMO · tanpa progres"
                      : draft.mode === "adventure"
                        ? `PETUALANGAN · BAB ${draft.chapter}`
                        : `${worlds.find((w) => w.id === active.world)?.name} · MISI ${active.number}`}
                  </span>
                  <span className="timer">
                    {Math.floor(draft.seconds / 60)}:
                    {String(draft.seconds % 60).padStart(2, "0")}
                  </span>
                </div>
                <div className="play-heading">
                  <h1>{active.title}</h1>
                  <p className="arabic" lang="ar" dir="rtl">
                    {active.titleAr}
                  </p>
                </div>
                {draft.phase === "study" ? (
                  <div className="study-layout">
                    <aside className="mission-card">
                      <span className="companion-avatar">
                        {active.world === "istima"
                          ? "🐰"
                          : active.world === "kalam"
                            ? "🐱"
                            : "🦊"}
                      </span>
                      <span className="eyebrow">
                        MISIMU BERSAMA {active.character.toUpperCase()}
                      </span>
                      <h2>Siapkan rasa ingin tahumu!</h2>
                      <p>{active.mission}</p>
                      <div className="objective">
                        <Flag size={18} />
                        <div>
                          <b>Yang akan kamu pelajari</b>
                          <p>{active.objective}</p>
                        </div>
                      </div>
                      <Scenery type={active.scene} />
                    </aside>
                    <div className="study-content">
                      <div className="sheet">
                        <span className="eyebrow">
                          {active.world === "istima"
                            ? "SATU CERITA UTUH · 10 PERTANYAAN"
                            : active.world === "kalam"
                              ? "SATU PERCAKAPAN · 10 JAWABAN LISAN"
                              : "SATU BACAAN UTUH · 10 PERTANYAAN"}
                        </span>
                        <h2>
                          {active.world === "istima"
                            ? "Pasang telingamu, cerita dimulai."
                            : active.world === "kalam"
                              ? "Kenalan dulu dengan misinya."
                              : "Buka halaman petualanganmu."}
                        </h2>
                        {active.world === "istima" ? (
                          <>
                            <div className="listen-illustration">
                              <Headphones size={58} />
                              <span>✦</span>
                              <i>♪</i>
                            </div>
                            <AudioPlayer
                              key={active.id}
                              text={active.textAr}
                              id={active.id}
                              label="Putar cerita lengkap"
                              sound={save.sound}
                              onPlay={bumpReplay}
                              onComplete={() =>
                                setDraft((d) => (d ? { ...d, heard: true } : d))
                              }
                            />
                            <p className="muted">
                              Dengarkan seluruh cerita dahulu. Teks dan
                              terjemahan akan terbuka setelah kamu menyelesaikan
                              10 pertanyaan.
                            </p>
                            {draft.heard && (
                              <p className="success-line">
                                <Check size={17} /> Cerita sudah selesai
                                didengarkan. Siap menjawab!
                              </p>
                            )}
                            {draft.demo && !draft.heard && (
                              <button
                                className="text-button"
                                onClick={() =>
                                  setDraft((d) =>
                                    d ? { ...d, heard: true } : d,
                                  )
                                }
                              >
                                Demo tanpa audio: lanjut untuk memeriksa soal
                              </button>
                            )}
                          </>
                        ) : (
                          <>
                            <p
                              className="arabic reading-text"
                              dir="rtl"
                              lang="ar"
                            >
                              {active.textAr}
                            </p>
                            {active.world === "kalam" && (
                              <AudioPlayer
                                key={active.id}
                                text={active.textAr}
                                id={active.id}
                                sound={save.sound}
                                label="Dengarkan Mimi"
                                onPlay={bumpReplay}
                              />
                            )}
                            <p className="muted">
                              {active.world === "qiraah"
                                ? "Baca dengan tenang. Teks tetap tersedia saat menjawab; terjemahan lengkap dibuka setelah evaluasi."
                                : active.textId}
                            </p>
                          </>
                        )}
                      </div>
                      <div className="sheet vocabulary-sheet">
                        <h3>
                          Kantong kosakata <span>🎒</span>
                        </h3>
                        <p>Kata baru untuk bekal perjalananmu.</p>
                        <div className="vocabulary">
                          {active.vocabulary.map((v) => (
                            <div key={v.ar}>
                              <span className="arabic" dir="rtl" lang="ar">
                                {v.ar}
                              </span>
                              <small>{v.id}</small>
                            </div>
                          ))}
                        </div>
                      </div>
                      <button
                        className="btn primary full"
                        disabled={active.world === "istima" && !draft.heard}
                        onClick={() => setDraft({ ...draft, phase: "quiz" })}
                      >
                        Aku siap! Mulai 10 tantangan <ArrowRight size={18} />
                      </button>
                    </div>
                  </div>
                ) : (
                  <div
                    className={`quiz-layout ${active.world === "qiraah" ? "with-text" : ""}`}
                  >
                    {active.world === "qiraah" && (
                      <aside className="sheet reading-aside">
                        <span className="eyebrow">
                          BACA KEMBALI PETUNJUKNYA
                        </span>
                        <p className="arabic reading-text" lang="ar" dir="rtl">
                          {active.textAr}
                        </p>
                      </aside>
                    )}
                    <div className="quiz-main">
                      <div className="quiz-progress">
                        <span>
                          Tantangan <b>{draft.answers.length + 1}</b> dari 10
                        </span>
                        <div className="progress-track">
                          <i
                            style={{
                              width: `${(draft.answers.length / 10) * 100}%`,
                            }}
                          />
                        </div>
                        <span>{draft.answers.length * 10}%</span>
                      </div>
                      <div className="sheet question-sheet">
                        <div className="character-dialog">
                          <span>
                            {active.world === "istima"
                              ? "🐰"
                              : active.world === "kalam"
                                ? "🐱"
                                : "🦊"}
                          </span>
                          <small>
                            {active.world === "kalam"
                              ? "Mimi ingin mendengar jawabanmu."
                              : active.world === "istima"
                                ? "Apa yang kamu dengar dalam cerita?"
                                : "Cari jawabannya di dalam bacaan."}
                          </small>
                        </div>
                        <h2 className="arabic question-ar" dir="rtl" lang="ar">
                          {current.ar}
                        </h2>
                        {active.world === "kalam" && active.number <= 3 && (
                          <p className="question-translation">
                            {current.translation}
                          </p>
                        )}
                        {active.world !== "qiraah" && (
                          <AudioPlayer
                            key={current.id}
                            id={current.id}
                            text={current.ar}
                            label="Dengarkan pertanyaan"
                            sound={save.sound}
                            onPlay={bumpReplay}
                          />
                        )}
                        {active.world === "kalam" ? (
                          <>
                            <Speaking
                              key={current.id}
                              question={current}
                              levelId={active.id}
                              context={draft.answers
                                .map((a) => a.transcript || "")
                                .join(" | ")}
                              onAnswer={submit}
                            />
                            {draft.demo && (
                              <details className="demo-answer">
                                <summary>
                                  Demo: lihat contoh respons lisan
                                </summary>
                                <p className="arabic" lang="ar" dir="rtl">
                                  {current.example}
                                </p>
                                <p>{current.explanationId}</p>
                                <button
                                  className="btn secondary"
                                  onClick={() =>
                                    submit({
                                      questionId: current.id,
                                      transcript: "",
                                      points: 0,
                                      exampleViewed: true,
                                    })
                                  }
                                >
                                  Lanjutkan demo (tanpa nilai)
                                </button>
                              </details>
                            )}
                          </>
                        ) : (
                          <>
                            <div className="answer-options">
                              {current.options!.map((o, i) => (
                                <button
                                  className={
                                    selected === i
                                      ? "answer-option selected"
                                      : "answer-option"
                                  }
                                  key={o}
                                  onClick={() => setSelected(i)}
                                  aria-pressed={selected === i}
                                >
                                  <span>{String.fromCharCode(65 + i)}</span>
                                  <b className="arabic" dir="rtl" lang="ar">
                                    {o}
                                  </b>
                                  <i>{selected === i && <Check size={18} />}</i>
                                </button>
                              ))}
                            </div>
                            <button
                              className="btn primary full"
                              disabled={selected === null}
                              onClick={() =>
                                selected !== null &&
                                submit({
                                  questionId: current.id,
                                  choice: selected,
                                  points: selected === current.answer ? 10 : 0,
                                })
                              }
                            >
                              {draft.answers.length === 9
                                ? "Selesaikan misi"
                                : "Simpan jawaban & lanjut"}{" "}
                              <ArrowRight size={18} />
                            </button>
                          </>
                        )}
                        <div className="question-tools">
                          <button
                            className="text-button"
                            onClick={() => {
                              if (!hint)
                                setDraft((d) =>
                                  d ? { ...d, hints: d.hints + 1 } : d,
                                );
                              setHint(!hint);
                            }}
                          >
                            <Lightbulb size={16} />{" "}
                            {hint ? "Tutup bantuan" : "Butuh bantuan kosakata?"}
                          </button>
                          <span>Tidak ada batas waktu. Kamu pasti bisa!</span>
                        </div>
                        {hint && (
                          <div className="hint-words">
                            {active.vocabulary.map((v) => (
                              <span key={v.ar}>
                                <b className="arabic" lang="ar" dir="rtl">
                                  {v.ar}
                                </b>{" "}
                                {v.id}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                      {active.world === "istima" && (
                        <details className="relisten">
                          <summary>Dengarkan kembali cerita utuh</summary>
                          <AudioPlayer
                            id={active.id + "-relisten"}
                            text={active.textAr}
                            sound={save.sound}
                            onPlay={bumpReplay}
                          />
                        </details>
                      )}
                    </div>
                  </div>
                )}
              </section>
            )}
            {view === "result" && result && resultLevel && (
              <section className="result-page">
                <div className="result-hero">
                  <motion.div
                    className="result-medal"
                    initial={{ scale: 0.4, rotate: -15 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ type: "spring" }}
                  >
                    {" "}
                    {result.score >= 60 ? "🏅" : "🌱"}
                  </motion.div>
                  <span className="eyebrow">
                    {result.demo
                      ? "HASIL LATIHAN DEMO"
                      : `MISI ${resultLevel.number} · ${resultLevel.title.toUpperCase()}`}
                  </span>
                  <h1>
                    {result.demo
                      ? "Penjelajahan demo selesai!"
                      : result.score >= 60
                        ? "Hebat! Misi ditaklukkan."
                        : "Setiap percobaan membuatmu tumbuh."}
                  </h1>
                  <p>
                    {result.demo
                      ? "Hasil demo tidak menambah bintang, koin, atau membuka level."
                      : result.score >= 60
                        ? `Kamu menemukan ${resultLevel.reward.toLowerCase()} pengetahuan. Ayo lanjutkan perjalanan!`
                        : "Coba lagi hingga nilai 60. Baca pembahasan di bawah untuk menemukan petunjuknya."}
                  </p>
                  <Stars count={result.stars} />
                  <div className="result-stats">
                    <div>
                      <b>
                        {result.score}
                        <small>/100</small>
                      </b>
                      <span>Nilai misi</span>
                    </div>
                    <div>
                      <b>
                        {Math.floor(result.seconds / 60)}:
                        {String(result.seconds % 60).padStart(2, "0")}
                      </b>
                      <span>Waktu belajar</span>
                    </div>
                    <div>
                      <b>{result.replays}</b>
                      <span>Pemutaran audio</span>
                    </div>
                    <div>
                      <b>{result.hints}</b>
                      <span>Bantuan kosakata</span>
                    </div>
                  </div>
                  <div className="button-row centered">
                    <button
                      className="btn secondary"
                      onClick={() =>
                        start(resultLevel, result.mode, result.demo)
                      }
                    >
                      <RotateCcw size={16} /> Coba lagi
                    </button>
                    {result.mode === "adventure" &&
                    !result.demo &&
                    result.score >= 60 ? (
                      <button
                        className="btn primary"
                        onClick={() => navigate("adventure")}
                      >
                        Lanjutkan cerita <ArrowRight size={17} />
                      </button>
                    ) : result.score >= 60 &&
                      !result.demo &&
                      resultLevel.number < 10 ? (
                      <button
                        className="btn primary"
                        onClick={() =>
                          start(
                            levels.find(
                              (l) =>
                                l.world === resultLevel.world &&
                                l.number === resultLevel.number + 1,
                            )!,
                          )
                        }
                      >
                        Misi berikutnya <ArrowRight size={17} />
                      </button>
                    ) : (
                      <button
                        className="btn primary"
                        onClick={() => openWorld(resultLevel.world)}
                      >
                        Kembali ke peta <Map size={17} />
                      </button>
                    )}
                  </div>
                </div>
                <div className="review-area">
                  <Tutor
                    key={result.id}
                    levelId={resultLevel.id}
                    score={result.score}
                  />
                  <h2>Bekal untuk perjalanan berikutnya</h2>
                  <details className="sheet" open>
                    <summary>Bacaan / skenario lengkap dan artinya</summary>
                    <p className="arabic reading-text" dir="rtl" lang="ar">
                      {resultLevel.textAr}
                    </p>
                    <p>{resultLevel.textId}</p>
                  </details>
                  {result.answers.map((a, i) => {
                    const q = resultLevel.questions[i];
                    return (
                      <details key={q.id} className="review-question sheet">
                        <summary>
                          <span
                            className={
                              a.points >= 6 ? "answer-correct" : "answer-wrong"
                            }
                          >
                            {i + 1}
                          </span>
                          <span className="arabic" dir="rtl" lang="ar">
                            {q.ar}
                          </span>
                          <b>{a.points}/10</b>
                        </summary>
                        <div className="review-detail">
                          {q.options && (
                            <>
                              <p>
                                Jawabanmu:{" "}
                                <span className="arabic" dir="rtl" lang="ar">
                                  {q.options[a.choice ?? 0]}
                                </span>
                              </p>
                              <p>
                                Jawaban benar:{" "}
                                <b className="arabic" dir="rtl" lang="ar">
                                  {q.options[q.answer!]}
                                </b>
                              </p>
                            </>
                          )}
                          {a.transcript && (
                            <p>
                              Responsmu:{" "}
                              <span className="arabic" dir="rtl" lang="ar">
                                {a.transcript}
                              </span>
                            </p>
                          )}
                          <p className="arabic" dir="rtl" lang="ar">
                            {q.explanationAr}
                          </p>
                          <p>{q.explanationId}</p>
                          {q.alternatives && (
                            <>
                              <p>
                                Contoh alternatif:{" "}
                                <span className="arabic" dir="rtl" lang="ar">
                                  {q.alternatives.join(" / ")}
                                </span>
                              </p>
                              <p>Kriteria: {q.criteria}</p>
                            </>
                          )}
                          {a.assessment && (
                            <>
                              <p>{a.assessment.feedback}</p>
                              <div className="rubric-review">
                                {(
                                  [
                                    "relevance",
                                    "vocabulary",
                                    "structure",
                                    "comprehensibility",
                                  ] as const
                                ).map((k, j) => (
                                  <span key={k}>
                                    {
                                      [
                                        "Relevansi",
                                        "Kosakata",
                                        "Struktur",
                                        "Keterpahaman",
                                      ][j]
                                    }{" "}
                                    <b>{a.assessment![k]}/100</b>
                                  </span>
                                ))}
                              </div>
                            </>
                          )}
                        </div>
                      </details>
                    );
                  })}
                </div>
              </section>
            )}
            {view === "progress" && (
              <section className="progress-page">
                <div className="page-heading">
                  <span className="eyebrow">JEJAK PENJELAJAHANMU</span>
                  <h1>Langkah kecil, kemajuan besar.</h1>
                  <p>
                    Setiap usaha tercatat. Nilai terbaik menentukan bintang dan
                    pembukaan level.
                  </p>
                </div>
                <div className="stat-grid">
                  <div>
                    <span>🏁</span>
                    <b>
                      {total.completed}
                      <small>/30</small>
                    </b>
                    <p>Misi ditaklukkan</p>
                  </div>
                  <div>
                    <span>⭐</span>
                    <b>
                      {total.stars}
                      <small>/90</small>
                    </b>
                    <p>Bintang terkumpul</p>
                  </div>
                  <div>
                    <span>🪙</span>
                    <b>{total.coins}</b>
                    <p>Koin petualangan</p>
                  </div>
                  <div>
                    <span>🎯</span>
                    <b>{allReal.length * 10}</b>
                    <p>Jawaban dikerjakan</p>
                  </div>
                </div>
                <div className="progress-columns">
                  <div className="sheet">
                    <h2>Penguasaan tiga dunia</h2>
                    <p>
                      Persentase dari rata-rata nilai terbaik 10 level di setiap
                      dunia.
                    </p>
                    {worlds.map((w) => {
                      const avg = Math.round(
                        levels
                          .filter((l) => l.world === w.id)
                          .reduce(
                            (n, l) => n + (bestAttempt(save, l.id)?.score ?? 0),
                            0,
                          ) / 10,
                      );
                      return (
                        <div className="mastery-row" key={w.id}>
                          <div>
                            <span>
                              {w.emoji} {w.name}
                            </span>
                            <b>{avg}%</b>
                          </div>
                          <div className="progress-track">
                            <i
                              style={{ width: `${avg}%`, background: w.color }}
                            />
                          </div>
                          <button
                            className="text-button"
                            onClick={() => openWorld(w.id)}
                          >
                            Latihan {w.title.toLowerCase()}{" "}
                            <ChevronRight size={14} />
                          </button>
                        </div>
                      );
                    })}
                  </div>
                  <div className="sheet badge-sheet">
                    <h2>Lemari penemuan</h2>
                    <div className="badge-grid">
                      {worlds.map((w) => (
                        <div
                          key={w.id}
                          className={
                            doneWorld.some((x) => x.id === w.id)
                              ? "badge earned"
                              : "badge"
                          }
                        >
                          <span>{w.emoji}</span>
                          <b>Penjaga {w.title}</b>
                          <small>
                            {doneWorld.some((x) => x.id === w.id)
                              ? "Medali dunia diperoleh"
                              : "Selesaikan 10 misi"}
                          </small>
                        </div>
                      ))}
                      <div
                        className={
                          total.completed === 30 ? "badge earned" : "badge"
                        }
                      >
                        <span>🏆</span>
                        <b>Penjelajah Sejati</b>
                        <small>
                          {total.completed === 30
                            ? "Semua dunia ditaklukkan"
                            : "Selesaikan 30 misi"}
                        </small>
                      </div>
                    </div>
                    <div className="collection">
                      <strong>Koleksi benda</strong>
                      <p>
                        {levels
                          .filter(
                            (l) => (bestAttempt(save, l.id)?.score ?? 0) >= 60,
                          )
                          .map(
                            (l) =>
                              `${l.reward} (${worlds.find((w) => w.id === l.world)?.name} ${l.number})`,
                          )
                          .join(" · ") ||
                          "Kompas, kristal, dan peti harta menunggumu di setiap misi."}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="sheet skill-detail">
                  <h2>Lebih dekat dengan kemampuanmu</h2>
                  <div className="skill-detail-grid">
                    {worlds.map((w) => (
                      <div key={w.id}>
                        <h3>
                          {w.emoji} {w.name}
                        </h3>
                        {w.id === "kalam"
                          ? (
                              [
                                "relevance",
                                "vocabulary",
                                "structure",
                                "comprehensibility",
                              ] as const
                            ).map((key, i) => {
                              const assessed = allReal
                                .filter((a) => a.levelId.startsWith("kalam-"))
                                .flatMap((a) => a.answers)
                                .filter((a) => a.assessment);
                              const avg = assessed.length
                                ? Math.round(
                                    assessed.reduce(
                                      (n, a) => n + a.assessment![key],
                                      0,
                                    ) / assessed.length,
                                  )
                                : null;
                              return (
                                <div className="skill-metric" key={key}>
                                  <span>
                                    {
                                      [
                                        "Relevansi",
                                        "Kosakata",
                                        "Struktur kalimat",
                                        "Keterpahaman respons",
                                      ][i]
                                    }
                                  </span>
                                  <b>{avg === null ? "—" : `${avg}%`}</b>
                                </div>
                              );
                            })
                          : [
                              "Tokoh dan kosakata",
                              "Informasi",
                              "Instruksi dan urutan",
                              "Konteks dan kesimpulan",
                            ].map((cat) => {
                              const records = allReal
                                .filter((a) => a.levelId.startsWith(w.id + "-"))
                                .flatMap((a) => a.answers)
                                .filter(
                                  (a) =>
                                    levels
                                      .find(
                                        (l) =>
                                          l.world === w.id &&
                                          l.questions.some(
                                            (q) => q.id === a.questionId,
                                          ),
                                      )
                                      ?.questions.find(
                                        (q) => q.id === a.questionId,
                                      )?.category === cat,
                                );
                              const avg = records.length
                                ? Math.round(
                                    (records.reduce((n, a) => n + a.points, 0) /
                                      records.length) *
                                      10,
                                  )
                                : null;
                              return (
                                <div className="skill-metric" key={cat}>
                                  <span>{cat}</span>
                                  <b>{avg === null ? "—" : `${avg}%`}</b>
                                </div>
                              );
                            })}
                      </div>
                    ))}
                  </div>
                  <p className="muted">
                    Rata-rata seluruh percobaan nyata. Keterpahaman AI
                    berdasarkan teks hasil transkripsi; penilaian lisan guru
                    berdasarkan rekaman.
                  </p>
                </div>
                <div className="sheet detailed-progress">
                  <div className="section-heading">
                    <h2>Catatan untukmu dan guru</h2>
                    <button className="btn secondary" onClick={exportCSV}>
                      <Download size={16} /> Unduh laporan CSV
                    </button>
                  </div>
                  <p>
                    Total latihan: {allReal.length} percobaan ·{" "}
                    {allReal.reduce(
                      (n, a) =>
                        n +
                        a.answers.filter(
                          (x) => x.choice !== undefined && x.points === 10,
                        ).length,
                      0,
                    )}{" "}
                    jawaban pilihan ganda benar ·{" "}
                    {allReal.reduce(
                      (n, a) =>
                        n +
                        a.answers.filter(
                          (x) => x.choice !== undefined && x.points === 0,
                        ).length,
                      0,
                    )}{" "}
                    jawaban pilihan ganda salah ·{" "}
                    {allReal.reduce(
                      (n, a) =>
                        n + a.answers.filter((x) => x.assessment).length,
                      0,
                    )}{" "}
                    respons lisan dinilai.
                  </p>
                  <p className="muted">
                    Durasi belajar aktif:{" "}
                    {Math.round(
                      allReal.reduce((n, a) => n + a.seconds, 0) / 60,
                    )}{" "}
                    menit · Pemutaran audio:{" "}
                    {allReal.reduce((n, a) => n + a.replays, 0)} · Bantuan:{" "}
                    {allReal.reduce((n, a) => n + a.hints, 0)}. Percobaan demo
                    dikecualikan.
                  </p>
                  <div className="table-scroll">
                    <table>
                      <thead>
                        <tr>
                          <th>Misi</th>
                          <th>Percobaan</th>
                          <th>Terbaik</th>
                          <th>Bintang</th>
                          <th>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {levels.map((l) => {
                          const best = bestAttempt(save, l.id);
                          return (
                            <tr key={l.id}>
                              <td>
                                <b>
                                  {worlds.find((w) => w.id === l.world)?.name}{" "}
                                  {l.number}
                                </b>
                                <span>{l.title}</span>
                              </td>
                              <td>
                                {
                                  allReal.filter((a) => a.levelId === l.id)
                                    .length
                                }
                              </td>
                              <td>
                                {best ? (
                                  <button
                                    className="score-link"
                                    onClick={() => {
                                      setResult(best);
                                      navigate("result");
                                    }}
                                    aria-label={`Lihat hasil ${l.title}`}
                                  >
                                    {best.score} ↗
                                  </button>
                                ) : (
                                  "—"
                                )}
                              </td>
                              <td>
                                <Stars count={best?.stars} />
                              </td>
                              <td>
                                {best?.stars
                                  ? "Selesai"
                                  : unlocked(save, l)
                                    ? "Tersedia"
                                    : "Terkunci"}
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              </section>
            )}
          </motion.div>
        </AnimatePresence>
      </main>
      <footer>
        <span className="brand-mini">
          <Compass size={18} /> THE LOST EXPEDITION
        </span>
        <p>Petualangan yang membuatmu berani belajar.</p>
        <button className="text-button" onClick={() => setSettings(true)}>
          Suara & privasi <ShieldCheck size={14} />
        </button>
      </footer>
      <nav className="mobile-nav">
        <button
          className={view === "home" ? "active" : ""}
          onClick={() => navigate("home")}
        >
          <Home size={21} />
          {t("home", "Beranda")}
        </button>
        <button
          className={view === "map" ? "active" : ""}
          onClick={() => openWorld(world)}
        >
          <Map size={21} />
          {t("map", "Dunia")}
        </button>
        <button
          className={view === "adventure" ? "active" : ""}
          onClick={() => navigate("adventure")}
        >
          <Compass size={21} />
          Petualangan
        </button>
        <button
          className={view === "progress" ? "active" : ""}
          onClick={() => navigate("progress")}
        >
          <ChartNoAxesColumnIncreasing size={21} />
          {t("progress", "Progres")}
        </button>
      </nav>
      {(settings || profile) && (
        <div
          className="modal-backdrop"
          onClick={() => {
            setSettings(false);
            setProfile(false);
          }}
        >
          <section
            ref={modalRef}
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-label={profile ? "Profil penjelajah" : "Pengaturan"}
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="icon-btn modal-close"
              onClick={() => {
                setSettings(false);
                setProfile(false);
              }}
              aria-label="Tutup"
            >
              <X />
            </button>
            {profile ? (
              <>
                <span className="eyebrow">PROFIL PENJELAJAH</span>
                <h2>Siapa nama panggilanmu?</h2>
                <p>
                  Pakai nama rekaan saja. Tidak perlu nama lengkap atau alamat.
                </p>
                <label className="field-label">
                  Nama panggilan
                  <input
                    maxLength={24}
                    value={save.nickname}
                    onChange={(e) =>
                      setSave({ ...save, nickname: e.target.value })
                    }
                  />
                </label>
                <div className="avatar-options">
                  {["🧭", "🦉", "🐰", "🐱", "🦊", "🚀", "🌻", "🐼"].map((a) => (
                    <button
                      className={save.avatar === a ? "active" : ""}
                      aria-label={`Pilih avatar ${a}`}
                      key={a}
                      onClick={() => setSave({ ...save, avatar: a })}
                    >
                      {a}
                    </button>
                  ))}
                </div>
                <button
                  className="btn primary full"
                  onClick={() => {
                    if (!save.nickname.trim())
                      setSave({ ...save, nickname: "Penjelajah" });
                    setProfile(false);
                  }}
                >
                  Siap menjelajah <ArrowRight size={18} />
                </button>
              </>
            ) : (
              <>
                <span className="eyebrow">ATUR PERJALANANMU</span>
                <h2>Pengaturan</h2>
                <div className="settings-row">
                  <div>
                    <b>Suara pembelajaran</b>
                    <small>Suara sintetis Arab atau rekaman guru.</small>
                  </div>
                  <button
                    className="btn secondary"
                    onClick={() => {
                      setSave({ ...save, sound: !save.sound });
                      window.speechSynthesis?.cancel();
                    }}
                  >
                    {save.sound ? <Volume2 size={18} /> : <VolumeX size={18} />}{" "}
                    {save.sound ? "Aktif" : "Nonaktif"}
                  </button>
                </div>
                <label className="field-label">
                  Bahasa navigasi
                  <select
                    value={save.lang}
                    onChange={(e) =>
                      setSave({ ...save, lang: e.target.value as "id" | "ar" })
                    }
                  >
                    <option value="id">Bahasa Indonesia</option>
                    <option value="ar">العربية + panduan Indonesia</option>
                  </select>
                </label>
                <details className="settings-details">
                  <summary>Layanan AI & audio server</summary>
                  <p>{services}</p>
                  <p>
                    Kunci API diatur pemilik website melalui Vercel. Token akses
                    berikut hanya berlaku di sesi perangkat ini.
                  </p>
                  <label className="field-label">
                    Token akses layanan
                    <input
                      type="password"
                      autoComplete="off"
                      value={audioToken}
                      onChange={(e) => setAudioToken(e.target.value)}
                      placeholder="Diberikan pengelola website"
                    />
                  </label>
                  <button
                    className="btn secondary"
                    onClick={() => {
                      sessionStorage.setItem("expedition-ai-token", audioToken);
                      setServices("Token akses disimpan untuk sesi ini.");
                    }}
                  >
                    Simpan token sesi
                  </button>
                  <p className="muted">
                    Tanpa layanan AI, gunakan suara Arab perangkat dan penilaian
                    rekaman bersama guru. Penilaian guru tetap memakai bobot
                    rubrik 40/25/20/15.
                  </p>
                </details>
                <details className="settings-details">
                  <summary>Cadangan & privasi</summary>
                  <p>
                    Progres tersimpan di browser ini. Menghapus data browser
                    dapat menghapus progres. Unduh cadangan untuk berpindah
                    perangkat.
                  </p>
                  <div className="button-row">
                    <button className="btn secondary" onClick={backup}>
                      <Download size={16} /> Unduh progres
                    </button>
                    <button
                      className="btn secondary"
                      onClick={() => importInput.current?.click()}
                    >
                      <Upload size={16} /> Pulihkan progres
                    </button>
                  </div>
                  <input
                    ref={importInput}
                    type="file"
                    accept="application/json,.json"
                    hidden
                    onChange={(e) => void restore(e.target.files?.[0])}
                  />
                  <p>
                    Rekaman suara bersifat sementara dan dihapus saat berganti
                    soal. Pengiriman ke layanan AI hanya dilakukan setelah
                    persetujuan pada soal. Nama panggilan tidak dikirim ke AI.
                  </p>
                  <button
                    className="text-button danger"
                    onClick={() => setReset(!reset)}
                  >
                    Atur ulang seluruh progres
                  </button>
                  {reset && (
                    <div className="notice">
                      <p>
                        Semua nilai dan bintang di perangkat ini akan dihapus.
                        Simpan cadangan dahulu jika diperlukan.
                      </p>
                      <div className="button-row">
                        <button
                          className="btn secondary"
                          onClick={() => setReset(false)}
                        >
                          Batal
                        </button>
                        <button
                          className="btn danger-btn"
                          onClick={() => {
                            preserveOriginal.current = false;
                            setStorageError("");
                            setSave(initialSave);
                            setDraft(null);
                            setResult(null);
                            setReset(false);
                            setSettings(false);
                            navigate("home");
                          }}
                        >
                          Hapus progres
                        </button>
                      </div>
                    </div>
                  )}
                </details>
                <details className="settings-details">
                  <summary>Mode demo · periksa semua 30 level</summary>
                  <p>
                    Untuk memeriksa materi dan alur. Hasil demo tidak membuka
                    level atau menambah penghargaan.
                  </p>
                  <div className="demo-levels">
                    {worlds.map((w) => (
                      <div key={w.id}>
                        <b>{w.name}</b>
                        <div>
                          {levels
                            .filter((l) => l.world === w.id)
                            .map((l) => (
                              <button
                                key={l.id}
                                onClick={() => {
                                  setSettings(false);
                                  start(l, "world", true);
                                }}
                                aria-label={`Demo ${w.name} level ${l.number}`}
                              >
                                {l.number}
                              </button>
                            ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </details>
              </>
            )}
          </section>
        </div>
      )}
    </div>
  );
}
