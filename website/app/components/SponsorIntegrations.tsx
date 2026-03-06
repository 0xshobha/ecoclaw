"use client";

import { motion } from "framer-motion";
import { DollarSign, ExternalLink } from "lucide-react";

const sponsors = [
  {
    name: "FLock.io",
    emoji: "🤖",
    bounty: "$5,000",
    category: "AI Agents for Good",
    description: "Federated climate LLM — cost-effective inference at scale",
    file: "skills/flock_llm.py",
    color: "#6366F1",
    href: "https://flock.io",
  },
  {
    name: "Z.AI",
    emoji: "⚡",
    bounty: "$4,000",
    category: "General AI",
    description: "Compound AI reasoning for impact forecasting",
    file: "skills/zai_llm.py",
    color: "#00D4FF",
    href: "https://z.ai",
  },
  {
    name: "Compression Co.",
    emoji: "🛰️",
    bounty: "£1,000",
    category: "Satellite Imagery",
    description: "SDK for NASA/ESA imagery analytics + NDVI charts",
    file: "skills/satellite.py",
    color: "#F59E0B",
    href: "#",
  },
  {
    name: "Animoca Brands",
    emoji: "🎮",
    bounty: "$1,000",
    category: "Web3 / BGA",
    description: "Base-chain alert hashes + ERC-721 NFT contributor rewards",
    file: "skills/animoca_web3.py",
    color: "#EC4899",
    href: "https://animocabrands.com",
  },
  {
    name: "Unibase",
    emoji: "🗄️",
    bounty: "Bonus",
    category: "On-Chain Storage",
    description: "Permanent decentralised payload storage via IPFS",
    file: "skills/unibase.py",
    color: "#10B981",
    href: "#",
  },
  {
    name: "Virtual Protocol",
    emoji: "🤝",
    bounty: "Bonus",
    category: "Agent Reputation",
    description: "On-chain agent action registry & NFT identity",
    file: "skills/virtual_protocol.py",
    color: "#8B5CF6",
    href: "#",
  },
  {
    name: "Imperial Blockchain",
    emoji: "🏛️",
    bounty: "$500 × 2",
    category: "Human-in-the-Loop",
    description: "Claw for Human + Human for Claw confirmation loops",
    file: "interfaces/telegram_bot.py",
    color: "#3B82F6",
    href: "#",
  },
  {
    name: "BGA",
    emoji: "🌱",
    bounty: "Prize",
    category: "Blockchain for Good",
    description: "Climate-tied good-cause on-chain evidence trail",
    file: "skills/animoca_web3.py",
    color: "#2A7A55",
    href: "#",
  },
];

export default function SponsorIntegrations() {
  return (
    <section id="integrations" className="py-24 px-6 bg-navy-dark circuit-bg">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <span className="inline-block px-3 py-1 text-xs font-medium tracking-widest uppercase text-teal bg-teal/10 rounded-full border border-teal/20 mb-4">
            Sponsor Integrations
          </span>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            8 Sponsors.{" "}
            <span className="gradient-text">One Ecosystem.</span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto text-lg">
            Every integration is a real skill file in the codebase — not a
            placeholder. Hover to see exactly how each sponsor is used.
          </p>
        </motion.div>

        {/* Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {sponsors.map((s, i) => (
            <motion.a
              key={s.name}
              href={s.href}
              target="_blank"
              rel="noopener noreferrer"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.45, delay: i * 0.07 }}
              whileHover={{ y: -6, scale: 1.02 }}
              className="group glass-card rounded-2xl p-5 flex flex-col gap-3 cursor-pointer
                hover:border-teal/25 transition-all duration-300 relative overflow-hidden"
            >
              {/* Teal border on hover */}
              <div
                className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl border border-teal/25"
              />

              {/* Top row */}
              <div className="flex items-start justify-between relative z-10">
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                  style={{ background: `${s.color}18`, border: `1px solid ${s.color}30` }}
                >
                  {s.emoji}
                </div>
                <div className="flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-full"
                  style={{ background: `${s.color}18`, color: s.color, border: `1px solid ${s.color}30` }}
                >
                  <DollarSign size={10} strokeWidth={2.5} />
                  {s.bounty}
                </div>
              </div>

              {/* Name + category */}
              <div className="relative z-10">
                <div className="flex items-center gap-1.5">
                  <h3 className="font-bold text-white text-base">{s.name}</h3>
                  <ExternalLink
                    size={12}
                    className="text-slate-500 group-hover:text-slate-300 transition-colors opacity-0 group-hover:opacity-100"
                  />
                </div>
                <p className="text-xs text-slate-500 mt-0.5">{s.category}</p>
              </div>

              {/* Description */}
              <p className="text-sm text-slate-400 leading-relaxed relative z-10 flex-1">
                {s.description}
              </p>

              {/* File badge */}
              <div
                className="text-[11px] font-mono px-2 py-1 rounded-md relative z-10 truncate"
                style={{ background: `${s.color}10`, color: `${s.color}cc`, border: `1px solid ${s.color}20` }}
              >
                📄 {s.file}
              </div>
            </motion.a>
          ))}
        </div>

        {/* Total bounty footer */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-12 text-center"
        >
          <div className="inline-flex items-center gap-3 px-8 py-4 rounded-2xl glass-card border border-teal/20">
            <span className="text-2xl">🏆</span>
            <div className="text-left">
              <div className="text-white font-bold text-lg">$10,000+ in Bounties Targeted</div>
              <div className="text-slate-400 text-sm">7+ sponsor integrations · UK AI Agent Hackathon EP4</div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
