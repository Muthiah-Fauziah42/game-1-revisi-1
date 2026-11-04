import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "The Lost Expedition — Petualangan Bahasa Arab",
  description:
    "Jelajahi Hutan Suara, Kota Percakapan, dan Kastil Cerita. 30 level bahasa Arab untuk anak SD/MI.",
  icons: { icon: "/icon.svg" },
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}
