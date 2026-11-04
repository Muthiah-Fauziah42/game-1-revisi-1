"use client";
import { useEffect, useRef, useState, useId } from "react";
import { Play, Pause, RotateCcw, Volume2 } from "lucide-react";
export default function AudioPlayer({
  text,
  id,
  label = "Dengarkan",
  onComplete,
  onPlay,
  sound = true,
}: {
  text: string;
  id: string;
  label?: string;
  onComplete?: () => void;
  onPlay?: () => void;
  sound?: boolean;
}) {
  const instanceId = useId();
  const [state, setState] = useState<"idle" | "playing" | "paused" | "loading">(
    "idle",
  );
  const [error, setError] = useState("");
  const [source, setSource] = useState("");
  const media = useRef<HTMLAudioElement | null>(null);
  const utter = useRef<SpeechSynthesisUtterance | null>(null);
  const url = useRef("");
  const dead = useRef(false);
  const complete = useRef(onComplete);
  complete.current = onComplete;
  useEffect(() => {
    dead.current = false;
    return () => {
      dead.current = true;
      window.speechSynthesis?.cancel();
      media.current?.pause();
      if (url.current) URL.revokeObjectURL(url.current);
    };
  }, [id]);
  useEffect(() => {
    if (!sound) {
      window.speechSynthesis?.cancel();
      media.current?.pause();
      setState("idle");
    }
  }, [sound]);
  useEffect(() => {
    const handle = (event: Event) => {
      if ((event as CustomEvent).detail !== instanceId) {
        media.current?.pause();
        setState("idle");
      }
    };
    window.addEventListener("expedition-audio", handle);
    return () => window.removeEventListener("expedition-audio", handle);
  }, [instanceId]);
  function stop() {
    window.speechSynthesis?.cancel();
    media.current?.pause();
    utter.current = null;
    media.current = null;
    setState("idle");
  }
  async function play(replay = false) {
    if (!sound) {
      setError("Aktifkan suara di Pengaturan untuk mendengarkan.");
      return;
    }
    setError("");
    if (state === "playing" && !replay) {
      if (media.current) media.current.pause();
      else window.speechSynthesis?.pause();
      setState("paused");
      return;
    }
    if (state === "paused" && !replay) {
      if (media.current) {
        try {
          await media.current.play();
        } catch {
          setError("Audio belum dapat dilanjutkan. Coba putar ulang.");
          return;
        }
      } else window.speechSynthesis?.resume();
      setState("playing");
      return;
    }
    window.dispatchEvent(
      new CustomEvent("expedition-audio", { detail: instanceId }),
    );
    stop();
    setState("loading");
    onPlay?.();
    const handleEnd = () => {
      if (!dead.current) {
        setState("idle");
        complete.current?.();
      }
    };
    const playMedia = async (src: string) => {
      const a = new Audio(src);
      media.current = a;
      a.onended = handleEnd;
      await a.play();
      if (dead.current) {
        a.pause();
        return;
      }
      setState("playing");
    };
    try {
      // Teacher-supplied recordings take precedence and work without any API key.
      const path = `/audio/${encodeURIComponent(id.replace(/-relisten$/, ""))}.mp3`;
      const check = await fetch(path, { method: "HEAD" });
      if (check.ok && check.headers.get("content-type")?.includes("audio")) {
        await playMedia(path);
        setSource("Rekaman materi");
        return;
      }
      const voice = window.speechSynthesis
        ?.getVoices()
        .find((v) => v.lang.toLowerCase().startsWith("ar"));
      if (voice) {
        const u = new SpeechSynthesisUtterance(text);
        u.lang = "ar-SA";
        u.voice = voice;
        u.rate = 0.82;
        u.onend = handleEnd;
        u.onerror = () => {
          if (!dead.current) {
            setState("idle");
            setError(
              "Pemutaran terhenti. Coba ulangi atau pilih layanan audio server.",
            );
          }
        };
        utter.current = u;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
        setSource("Suara sintetis Arab perangkat");
        setState("playing");
        return;
      }
      const token = sessionStorage.getItem("expedition-ai-token") || "";
      const response = await fetch("/api/speech", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-AI-Access": token },
        body: JSON.stringify({ id }),
      });
      if (!response.ok)
        throw new Error(
          "Suara Arab belum tersedia di perangkat ini. Pasang suara Arab, tambahkan rekaman materi, atau aktifkan layanan audio server di Pengaturan.",
        );
      if (url.current) URL.revokeObjectURL(url.current);
      url.current = URL.createObjectURL(await response.blob());
      await playMedia(url.current);
      setSource("Suara buatan AI");
    } catch (e) {
      if (!dead.current) {
        setState("idle");
        setError(e instanceof Error ? e.message : "Audio belum tersedia.");
      }
    }
  }
  return (
    <div className="audio-box">
      <div className="audio-controls">
        <button
          className="btn audio-primary"
          onClick={() => void play()}
          disabled={state === "loading"}
          aria-label={
            state === "playing"
              ? "Jeda audio"
              : state === "paused"
                ? "Lanjutkan audio"
                : label
          }
        >
          {state === "playing" ? <Pause size={19} /> : <Play size={19} />}{" "}
          {state === "loading"
            ? "Menyiapkan…"
            : state === "playing"
              ? "Jeda"
              : state === "paused"
                ? "Lanjutkan"
                : label}
        </button>
        <button
          className="icon-btn"
          aria-label="Putar ulang dari awal"
          onClick={() => void play(true)}
          disabled={state === "loading"}
        >
          <RotateCcw size={19} />
        </button>
        <span className="sound-wave" aria-hidden="true">
          <i />
          <i />
          <i />
          <i />
          <i />
        </span>
      </div>
      <small>
        <Volume2 size={13} />{" "}
        {source || "Audio Bahasa Arab · dengarkan sampai selesai"}
      </small>
      {error && (
        <p className="notice" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
