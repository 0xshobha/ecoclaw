"use client";

import { motion } from "framer-motion";
import { Play, Send, Terminal, MessageSquare } from "lucide-react";

const commands = [
  {
    cmd: "/scan amazon deforestation",
    response: "🛰️ Fetching NASA imagery… NDVI Δ = -12.4% detected. Risk: HIGH. Minting alert NFT…",
  },
  {
    cmd: "/scan floods uk",
    response: "⚡ Z.AI forecast: Flood probability 87% in Thames Valley. On-chain CID: Qm3x…8f",
  },
  {
    cmd: "/status",
    response: "✅ Last scan: 2 min ago · 3 events detected · 1 NFT minted · Unibase CID stored",
  },
];

export default function LiveDemo() {
  return (
    <section id="demo" className="py-24 px-6 bg-navy-dark">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block px-3 py-1 text-xs font-medium tracking-widest uppercase text-teal bg-teal/10 rounded-full border border-teal/20 mb-4">
            Live Demo
          </span>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            See EcoClaw{" "}
            <span className="gradient-text">In Action</span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto text-lg">
            Watch the full 4-agent pipeline run in real time — from satellite
            query to on-chain alert in under 30 seconds.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 items-start">
          {/* Video placeholder */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="relative group"
          >
            <div className="relative aspect-video rounded-2xl overflow-hidden glass-card border border-teal/15">
              {/* Mock video thumbnail */}
              <div className="absolute inset-0 bg-navy-dark flex flex-col items-center justify-center gap-4">
                {/* Fake waveform bars */}
                <div className="flex items-end gap-1 h-12 mb-2">
                  {[40, 65, 35, 80, 55, 90, 45, 70, 60, 50, 85, 40].map((h, idx) => (
                    <motion.div
                      key={idx}
                      className="w-1.5 bg-teal/60 rounded-full"
                      style={{ height: `${h}%` }}
                      animate={{ height: [`${h}%`, `${Math.max(20, h - 20)}%`, `${h}%`] }}
                      transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        delay: idx * 0.1,
                        ease: "easeInOut",
                      }}
                    />
                  ))}
                </div>

                <div className="flex items-center gap-3 text-sm text-teal font-mono">
                  <span className="w-2 h-2 rounded-full bg-teal animate-pulse" />
                  NDVI Analysis Running…
                </div>

                {/* Play button overlay */}
                <a
                  href="https://youtu.be/your-demo-link"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="absolute inset-0 flex items-center justify-center group/play"
                >
                  <div className="w-16 h-16 rounded-full bg-teal/90 hover:bg-teal group/play-hover:scale-110 transition-all flex items-center justify-center glow-teal">
                    <Play size={24} className="text-navy ml-1" fill="currentColor" />
                  </div>
                </a>
              </div>

              {/* Corner labels */}
              <div className="absolute top-3 left-3 flex items-center gap-1.5 px-2.5 py-1 bg-red-500/80 rounded-full text-white text-xs font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
                LIVE DEMO
              </div>
              <div className="absolute bottom-3 right-3 text-xs text-slate-400 font-mono">
                2:47 duration
              </div>
            </div>

            <p className="text-center text-slate-500 text-sm mt-3">
              Demo video · Replace with your Loom/YouTube link
            </p>
          </motion.div>

          {/* Telegram console mock */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="flex flex-col gap-4"
          >
            {/* Terminal window */}
            <div className="glass-card rounded-2xl overflow-hidden border border-teal/15">
              {/* Title bar */}
              <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-700/50 bg-navy-dark/60">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-red-500/70" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500/70" />
                  <div className="w-3 h-3 rounded-full bg-green-500/70" />
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-400 ml-2">
                  <Terminal size={12} />
                  <span>@EcoClawBot — Telegram</span>
                </div>
              </div>

              {/* Chat messages */}
              <div className="p-4 space-y-4 font-mono text-sm">
                {commands.map((c, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -10 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.3 + i * 0.2 }}
                    className="space-y-1.5"
                  >
                    {/* User message */}
                    <div className="flex items-start gap-2 justify-end">
                      <div className="bg-teal/15 border border-teal/20 rounded-xl rounded-tr-sm px-3 py-2 text-teal text-xs max-w-[80%]">
                        {c.cmd}
                      </div>
                      <div className="w-7 h-7 rounded-full bg-slate-600 flex items-center justify-center text-xs flex-shrink-0">
                        👤
                      </div>
                    </div>
                    {/* Bot response */}
                    <div className="flex items-start gap-2">
                      <div className="w-7 h-7 rounded-full bg-forest/50 flex items-center justify-center text-sm flex-shrink-0">
                        🌍
                      </div>
                      <div className="bg-navy-light border border-slate-700/50 rounded-xl rounded-tl-sm px-3 py-2 text-slate-300 text-xs max-w-[80%]">
                        {c.response}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* CTA */}
            <div className="flex flex-col sm:flex-row gap-3">
              <a
                href="https://t.me/ecoclaw_bot"
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 flex items-center justify-center gap-2 py-3 px-5 rounded-xl
                  bg-teal text-navy font-semibold text-sm hover:bg-teal-dim
                  glow-teal transition-all duration-200 hover:scale-105"
              >
                <Send size={16} />
                Open in Telegram
              </a>
              <a
                href="#how-it-works"
                className="flex-1 flex items-center justify-center gap-2 py-3 px-5 rounded-xl
                  border border-slate-600 hover:border-teal/40 text-slate-300 hover:text-white
                  text-sm transition-all duration-200"
              >
                <MessageSquare size={16} />
                Explore Commands
              </a>
            </div>

            {/* Command list */}
            <div className="glass-card rounded-xl p-4 text-xs text-slate-400 font-mono space-y-1.5">
              {[
                ["/scan [region] [threat]", "Run full 4-agent pipeline"],
                ["/status", "Show last scan summary"],
                ["/register 0x…", "Link wallet for NFT rewards"],
                ["/agents", "List loaded agents"],
              ].map(([cmd, desc]) => (
                <div key={cmd} className="flex gap-3">
                  <span className="text-teal whitespace-nowrap">{cmd}</span>
                  <span className="text-slate-600">—</span>
                  <span>{desc}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
