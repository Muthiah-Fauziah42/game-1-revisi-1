"use client";
import { useEffect, useRef, useState } from "react";
import { Mic, Square, RefreshCw, Send, Check } from "lucide-react";
import type { Answer, Assessment, Question } from "@/lib/types";
import { rubricPoints } from "@/lib/game";
// The recognition API is nonstandard. Keep its narrow interface local.
interface Recognition {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  onresult:
    | ((e: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void)
    | null;
  onerror: ((e: { error: string }) => void) | null;
  onend: (() => void) | null;
  start: () => void;
  stop: () => void;
  abort: () => void;
}
type RecognitionConstructor = new () => Recognition;
export default function Speaking({
  question,
  levelId,
  context,
  onAnswer,
}: {
  question: Question;
  levelId: string;
  context: string;
  onAnswer: (a: Answer) => void;
}) {
  const [recording, setRecording] = useState(false);
  const [clip, setClip] = useState("");
  const [transcript, setTranscript] = useState("");
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);
  const [teacher, setTeacher] = useState(false);
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [consent, setConsent] = useState(false);
  const [ratings, setRatings] = useState([0, 0, 0, 0]);
  const recorder = useRef<MediaRecorder | null>(null);
  const stream = useRef<MediaStream | null>(null);
  const rec = useRef<Recognition | null>(null);
  const chunks = useRef<Blob[]>([]);
  const blob = useRef<Blob | null>(null);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const alive = useRef(true);
  const clipRef = useRef("");
  useEffect(() => {
    alive.current = true;
    return () => {
      alive.current = false;
      if (timer.current) clearTimeout(timer.current);
      if (recorder.current?.state === "recording") recorder.current.stop();
      rec.current?.abort();
      stream.current?.getTracks().forEach((t) => t.stop());
      if (clipRef.current) URL.revokeObjectURL(clipRef.current);
    };
  }, []);
  function stop() {
    if (timer.current) clearTimeout(timer.current);
    rec.current?.stop();
    if (recorder.current?.state === "recording") recorder.current.stop();
    stream.current?.getTracks().forEach((t) => t.stop());
    setRecording(false);
  }
  async function start() {
    setStatus("");
    setAssessment(null);
    setTranscript("");
    setTeacher(false);
    try {
      if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder)
        throw new Error(
          "Perekaman tidak didukung. Gunakan Chrome/Edge melalui HTTPS atau localhost.",
        );
      const s = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (!alive.current) {
        s.getTracks().forEach((t) => t.stop());
        return;
      }
      stream.current = s;
      chunks.current = [];
      blob.current = null;
      const mime = ["audio/webm;codecs=opus", "audio/mp4", "audio/webm"].find(
        (t) => MediaRecorder.isTypeSupported(t),
      );
      const r = new MediaRecorder(s, mime ? { mimeType: mime } : undefined);
      recorder.current = r;
      r.ondataavailable = (e) => {
        if (e.data.size) chunks.current.push(e.data);
      };
      r.onstop = () => {
        s.getTracks().forEach((t) => t.stop());
        if (!alive.current) return;
        const b = new Blob(chunks.current, { type: r.mimeType });
        blob.current = b;
        if (clipRef.current) URL.revokeObjectURL(clipRef.current);
        clipRef.current = URL.createObjectURL(b);
        setClip(clipRef.current);
        setRecording(false);
      };
      r.start();
      setRecording(true);
      const ctor = window as unknown as {
        SpeechRecognition?: RecognitionConstructor;
        webkitSpeechRecognition?: RecognitionConstructor;
      };
      const R = ctor.SpeechRecognition || ctor.webkitSpeechRecognition;
      if (R) {
        const speech = new R();
        rec.current = speech;
        speech.lang = "ar-SA";
        speech.interimResults = false;
        speech.continuous = true;
        speech.onresult = (e) => {
          if (alive.current)
            setTranscript(
              Array.from(e.results)
                .map((x) => x[0].transcript)
                .join(" "),
            );
        };
        speech.onerror = (e) => {
          if (alive.current)
            setStatus(
              `Pengenalan suara belum berhasil (${e.error}). Rekaman tetap bisa dinilai guru atau ditranskripsikan server.`,
            );
        };
        try {
          speech.start();
        } catch {
          setStatus("Rekaman aktif. Transkripsi perangkat tidak tersedia.");
        }
      } else
        setStatus(
          "Pengenalan suara perangkat tidak tersedia. Gunakan transkripsi server atau penilaian guru.",
        );
      timer.current = setTimeout(stop, 60000);
    } catch (e) {
      setStatus(e instanceof Error ? e.message : "Izin mikrofon diperlukan.");
      stream.current?.getTracks().forEach((t) => t.stop());
      setRecording(false);
    }
  }
  async function transcribe() {
    if (!blob.current || !consent) return;
    setBusy(true);
    setStatus("");
    try {
      const form = new FormData();
      const ext = blob.current.type.includes("mp4") ? "m4a" : "webm";
      form.append("file", blob.current, `jawaban.${ext}`);
      const r = await fetch("/api/transcribe", {
        method: "POST",
        headers: {
          "X-AI-Access": sessionStorage.getItem("expedition-ai-token") || "",
        },
        body: form,
      });
      const data = await r.json();
      if (!r.ok) throw new Error(data.error || "Transkripsi belum tersedia.");
      setTranscript(data.text);
    } catch (e) {
      setStatus(e instanceof Error ? e.message : "Transkripsi gagal.");
    } finally {
      setBusy(false);
    }
  }
  async function evaluate() {
    setBusy(true);
    setStatus("");
    try {
      const r = await fetch("/api/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-AI-Access": sessionStorage.getItem("expedition-ai-token") || "",
        },
        body: JSON.stringify({
          levelId,
          questionId: question.id,
          transcript,
          context,
        }),
      });
      const data = await r.json();
      if (!r.ok) throw new Error(data.error || "Evaluasi AI belum tersedia.");
      setAssessment(data);
    } catch (e) {
      setStatus(
        e instanceof Error
          ? e.message
          : "Evaluasi gagal. Gunakan penilaian guru.",
      );
    } finally {
      setBusy(false);
    }
  }
  const labels = [
    "Relevansi · 40%",
    "Kosakata · 25%",
    "Struktur · 20%",
    "Keterpahaman · 15%",
  ];
  return (
    <div className="speaking">
      <div className="mic-panel">
        <button
          className={`mic-button ${recording ? "recording" : ""}`}
          onClick={recording ? stop : () => void start()}
          disabled={busy}
          aria-label={recording ? "Selesai merekam" : "Mulai merekam jawaban"}
        >
          {recording ? <Square /> : <Mic size={30} />}
        </button>
        <strong>
          {recording ? "Aku sedang mendengarkan…" : "Giliranmu berbicara!"}
        </strong>
        <p>
          {recording
            ? "Tekan kotak untuk selesai. Maksimal 60 detik."
            : "Tekan mikrofon, izinkan akses, lalu jawab dalam Bahasa Arab."}
        </p>
      </div>
      <p className="privacy-note">
        Rekaman disimpan sementara di halaman ini dan tidak dikirim otomatis.
        Pengenalan suara browser dapat memakai layanan penyedia browser.
        Mintalah pendampingan orang dewasa.
      </p>
      {clip && !recording && (
        <>
          <audio controls src={clip} className="recorded-audio" />
          <div className="transcript">
            <small>Hasil pengenalan suara (bukan ukuran pelafalan)</small>
            <p className="arabic" dir="rtl" lang="ar">
              {transcript || "—"}
            </p>
          </div>
          <label className="check-label">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
            />{" "}
            Dengan pendampingan guru/orang tua, saya setuju mengirim rekaman
            atau teks ke layanan AI untuk jawaban ini.
          </label>
          <div className="button-row">
            <button
              className="btn secondary"
              disabled={!consent || busy}
              onClick={() => void transcribe()}
            >
              {busy ? "Memproses…" : "Transkripsi server"}
            </button>
            <button
              className="btn secondary"
              disabled={!transcript || !consent || busy}
              onClick={() => void evaluate()}
            >
              <Send size={16} /> Evaluasi AI
            </button>
            <button
              className="btn secondary"
              disabled={busy}
              onClick={() => setTeacher(!teacher)}
            >
              Nilai bersama guru
            </button>
          </div>
          {teacher && (
            <div className="teacher-panel">
              <strong>Penilaian guru/pendamping</strong>
              <p>
                Dengarkan rekaman, lalu nilai setiap aspek (0–100). Jawaban yang
                berbeda tetapi benar tetap diterima.
              </p>
              <p className="arabic" dir="rtl" lang="ar">
                Contoh: {question.example}
              </p>
              <p>{question.explanationId}</p>
              <p>Kriteria: {question.criteria}</p>
              {labels.map((l, i) => (
                <label className="range-label" key={l}>
                  {l}
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    value={ratings[i]}
                    onChange={(e) =>
                      setRatings((a) =>
                        a.map((v, j) => (i === j ? Number(e.target.value) : v)),
                      )
                    }
                  />
                  <b>{ratings[i]}</b>
                </label>
              ))}
              <button
                className="btn secondary"
                onClick={() =>
                  setAssessment({
                    relevance: ratings[0],
                    vocabulary: ratings[1],
                    structure: ratings[2],
                    comprehensibility: ratings[3],
                    feedback:
                      "Dinilai guru/pendamping berdasarkan rekaman dan rubrik.",
                    source: "teacher",
                  })
                }
              >
                <Check size={16} /> Simpan penilaian guru
              </button>
            </div>
          )}
          {assessment && (
            <div className="notice success">
              <strong>
                {rubricPoints(assessment)} / 10 ·{" "}
                {assessment.source === "ai"
                  ? "Evaluasi AI dari teks"
                  : "Penilaian guru"}
              </strong>
              <p>{assessment.feedback}</p>
              {assessment.correction && (
                <p className="arabic" dir="rtl" lang="ar">
                  {assessment.correction}
                </p>
              )}
              <p>
                AI menilai keterpahaman teks hasil pengenalan suara, bukan
                ketepatan pelafalan. Guru dapat meninjau hasilnya.
              </p>
              <button
                className="btn primary"
                disabled={busy}
                onClick={() =>
                  onAnswer({
                    questionId: question.id,
                    transcript,
                    assessment,
                    points: rubricPoints(assessment),
                  })
                }
              >
                Simpan jawaban & lanjut <Check size={18} />
              </button>
            </div>
          )}
        </>
      )}
      {status && (
        <p className="notice" role="status">
          {status}
        </p>
      )}
      <button
        className="text-button"
        onClick={() => {
          stop();
          setClip("");
          setTranscript("");
          setAssessment(null);
          setTeacher(false);
        }}
      >
        <RefreshCw size={14} /> Ulangi jawaban
      </button>
    </div>
  );
}
