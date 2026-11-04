"use client";
import { useState } from "react";
import { Sparkles } from "lucide-react";
export default function Tutor({
  levelId,
  score,
}: {
  levelId: string;
  score: number;
}) {
  const [data, setData] = useState<{
    tipId: string;
    practiceAr: string;
    practiceId: string;
    nextStepId: string;
  } | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function ask() {
    setBusy(true);
    setError("");
    try {
      const r = await fetch("/api/tutor", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-AI-Access": sessionStorage.getItem("expedition-ai-token") || "",
        },
        body: JSON.stringify({ levelId, score }),
      });
      const d = await r.json();
      if (!r.ok) throw new Error(d.error || "Saran belum tersedia.");
      setData(d);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Saran belum tersedia.");
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="sheet tutor-sheet">
      <span className="eyebrow">BURUNG HANTU PEMANDU</span>
      <h3>Latihan kecil, langkah berikutnya.</h3>
      <p>
        Ulangi kosakata yang masih sulit, lalu pakai dalam satu kalimat. Guru
        dapat mengaktifkan AI untuk saran dan variasi dialog sesuai hasilmu.
      </p>
      <button
        className="btn secondary"
        onClick={() => void ask()}
        disabled={busy}
      >
        <Sparkles size={16} />
        {busy ? "Menyiapkan saran…" : "Minta saran latihan AI"}
      </button>
      {error && (
        <p className="notice" role="status">
          {error}
        </p>
      )}
      {data && (
        <div className="notice success">
          <p>{data.tipId}</p>
          <p className="arabic" lang="ar" dir="rtl">
            {data.practiceAr}
          </p>
          <p>{data.practiceId}</p>
          <b>{data.nextStepId}</b>
          <p>
            Latihan tambahan buatan AI · mintalah guru meninjau bila ada yang
            kurang jelas.
          </p>
        </div>
      )}
    </div>
  );
}
