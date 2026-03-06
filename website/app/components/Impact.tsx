"use client";

import { motion } from "framer-motion";
import { Trophy, Zap, Calendar, Target } from "lucide-react";

const bounties = [
  { sponsor: "FLock.io", amount: "$5,000", tag: "AI Agents for Good", color: "#6366F1" },
  { sponsor: "Z.AI", amount: "$4,000", tag: "General AI", color: "#00D4FF" },
  { sponsor: "Compression Co.", amount: "£1,000", tag: "Satellite Imagery", color: "#F59E0B" },
  { sponsor: "Animoca / BGA", amount: "$1,000", tag: "Web3 Good", color: "#EC4899" },
  { sponsor: "Imperial (×2)", amount: "$1,000", tag: "Human-in-Loop", color: "#3B82F6" },
  { sponsor: "Unibase", amount: "Bonus", tag: "Storage", color: "#10B981" },
  { sponsor: "Virtual Protocol", amount: "Bonus", tag: "Agent NFT", color: "#8B5CF6" },
];

export default function Impact() {
  return (
    <section id="impact" className="py-24 px-6 bg-navy circuit-bg">
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
            Hackathon Impact
          </span>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Built to Win.{" "}
            <span className="gradient-text">Built to Matter.</span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto text-lg">
            EcoClaw targets 7+ sponsor bounties while solving a real problem —
            because winning and doing good aren&apos;t mutually exclusive.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Left: bounty breakdown */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="glass-card rounded-2xl p-6"
          >
            <h3 className="font-bold text-white text-lg mb-5 flex items-center gap-2">
              <Trophy size={20} className="text-yellow-400" />
              Bounty Breakdown
            </h3>
            <div className="space-y-3">
              {bounties.map((b, i) => (
                <motion.div
                  key={b.sponsor}
                  initial={{ opacity: 0, x: -15 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.07 }}
                  className="flex items-center gap-3"
                >
                  <div
                    className="w-2 h-2 rounded-full flex-shrink-0"
                    style={{ background: b.color }}
                  />
                  <div className="flex-1 flex items-center justify-between gap-3">
                    <span className="text-slate-300 text-sm">{b.sponsor}</span>
                    <div className="flex items-center gap-2">
                      <span
                        className="text-xs px-2 py-0.5 rounded"
                        style={{ background: `${b.color}15`, color: b.color }}
                      >
                        {b.tag}
                      </span>
                      <span className="text-white font-bold text-sm font-mono whitespace-nowrap">
                        {b.amount}
                      </span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Total */}
            <div className="mt-6 pt-5 border-t border-slate-700/50 flex items-center justify-between">
              <span className="text-slate-400 text-sm">Total potential</span>
              <span className="text-teal font-black text-2xl text-glow-teal">$10,000+</span>
            </div>
          </motion.div>

          {/* Right: event info + stats */}
          <div className="flex flex-col gap-5">
            {/* Event card */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="glass-card rounded-2xl p-6 border-teal/25"
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-teal/15 border border-teal/25 flex items-center justify-center flex-shrink-0">
                  <Calendar size={22} className="text-teal" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg">
                    UK AI Agent Hackathon EP4
                  </h3>
                  <p className="text-teal text-sm font-medium mt-0.5">× OpenClaw · March 2026</p>
                  <p className="text-slate-400 text-sm mt-2 leading-relaxed">
                    48-hour sprint building production AI agents for good — climate
                    monitoring, federated learning and on-chain incentives.
                  </p>
                </div>
              </div>
            </motion.div>

            {/* Stats grid */}
            {[
              {
                icon: Zap,
                label: "Sponsor Integrations",
                value: "7+",
                sub: "Each with real skill files",
                color: "#00D4FF",
              },
              {
                icon: Target,
                label: "Agents in Swarm",
                value: "4",
                sub: "Fetcher · Analyzer · Predictor · Web3",
                color: "#2A7A55",
              },
            ].map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 + i * 0.1 }}
                className="glass-card rounded-2xl p-5 flex items-center gap-4"
              >
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                  style={{ background: `${stat.color}18`, border: `1px solid ${stat.color}30` }}
                >
                  <stat.icon size={22} style={{ color: stat.color }} />
                </div>
                <div>
                  <div
                    className="text-3xl font-black"
                    style={{ color: stat.color, textShadow: `0 0 20px ${stat.color}55` }}
                  >
                    {stat.value}
                  </div>
                  <div className="text-white font-semibold text-sm">{stat.label}</div>
                  <div className="text-slate-400 text-xs mt-0.5">{stat.sub}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
