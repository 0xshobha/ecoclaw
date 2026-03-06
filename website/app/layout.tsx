import type { Metadata } from "next";
import { Space_Grotesk, Space_Mono } from "next/font/google";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({
  variable: "--font-space-grotesk",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
});

const spaceMono = Space_Mono({
  variable: "--font-space-mono",
  subsets: ["latin"],
  weight: ["400", "700"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://ecoclaw.io"),
  title: "EcoClaw — Autonomous Climate Agents That Actually Act",
  description:
    "Satellite-powered multi-agent swarm that detects climate threats, predicts impacts, posts on-chain alerts and mints NFT rewards in real time. Built for UK AI Agent Hackathon EP4 × OpenClaw.",
  keywords: [
    "EcoClaw",
    "climate AI",
    "multi-agent",
    "satellite imagery",
    "blockchain",
    "FLock",
    "Z.AI",
    "OpenClaw",
    "NDVI",
    "deforestation",
    "NFT rewards",
  ],
  authors: [{ name: "EcoClaw Team" }],
  openGraph: {
    title: "EcoClaw — Autonomous Climate Agents That Actually Act",
    description:
      "Real-time climate monitoring powered by AI agents, satellite data and Web3 incentives.",
    type: "website",
    siteName: "EcoClaw",
  },
  twitter: {
    card: "summary_large_image",
    title: "EcoClaw — Autonomous Climate Agents",
    description:
      "Satellite-powered multi-agent swarm detecting climate threats & minting NFT rewards.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body
        className={`${spaceGrotesk.variable} ${spaceMono.variable} antialiased bg-navy text-slate-100`}
      >
        {children}
      </body>
    </html>
  );
}
