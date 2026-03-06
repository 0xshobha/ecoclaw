"use client";

import { motion } from "framer-motion";
import {
  Satellite,
  BarChart2,
  Brain,
  Link2,
  ArrowRight,
  Database,
  Cpu,
} from "lucide-react";

const steps = [
  {
    number: "01",
    icon: Satellite,
    title: "Fetcher Agent",
    subtitle: "Data Acquisition",
    description:
      "Continuously polls NASA EONET, ESA Sentinel APIs and Compression Company SDK for live satellite imagery covering climate hotspots worldwide.",
    tags: ["NASA EONET", "ESA Sentinel", "Compression SDK"],
    color: "teal",
    glowColor: "#00D4FF",
  },
  {
    number: "02",
    icon: BarChart2,
    title: "Analyzer Agent",
    subtitle: "NDVI Change Detection",
    description:
      "Processes raw imagery with NumPy-based NDVI analysis, detects pixel-level vegetation change and generates normalised risk scores with chart outputs.",
    tags: ["NDVI Analysis", "Change Detection", "Risk Scoring"],
    color: "forest-light",
    glowColor: "#2A7A55",
  },
  {
    number: "03",
    icon: Brain,
    title: "Predictor Agent",
    subtitle: "AI Reasoning",
    description:
      "Feeds analysis into FLock.io federated LLM + Z.AI compound reasoning to forecast impact, estimate severity and generate human-readable alerts.",
    tags: ["FLock.io LLM", "Z.AI Reasoning", "Impact Forecast"],
    color: "teal",
    glowColor: "#00D4FF",
  },
  {
    number: "04",
    icon: Link2,
    title: "Web3 Coordinator",
    subtitle: "On-Chain Actions",
    description:
      "Mints Animoca NFT rewards, stores evidence payload on Unibase (IPFS), registers agent action on Virtual Protocol — all verified on Base chain.",
    tags: ["Animoca NFT", "Unibase IPFS", "Virtual Protocol"],
    color: "forest-light",
    glowColor: "#2A7A55",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 px-6 bg-navy">
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
            Architecture
          </span>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            How{" "}
            <span className="gradient-text">EcoClaw Works</span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto text-lg">
            Four specialized agents chained by the EcoClawOrchestrator — from
            raw satellite pixels to on-chain proof in one pipeline.
          </p>
        </motion.div>

        {/* Pipeline flow */}
        <div className="relative">
          {/* Desktop connector line */}
          <div className="hidden lg:block absolute top-[76px] left-[12.5%] right-[12.5%] h-px">
            <motion.div
              initial={{ scaleX: 0 }}
              whileInView={{ scaleX: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 1.2, delay: 0.3, ease: "easeInOut" }}
              style={{ transformOrigin: "left" }}
              className="h-full bg-teal/40"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((step, i) => (
              <motion.div
                key={step.number}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.15 }}
                className="relative group"
              >
                {/* Arrow between (mobile/tablet) */}
                {i < steps.length - 1 && (
                  <div className="lg:hidden flex justify-center my-3 text-slate-600">
                    <ArrowRight size={18} />
                  </div>
                )}

                <div
                  className="glass-card rounded-2xl p-6 h-full flex flex-col gap-4
                    hover:border-teal/30 hover:scale-[1.02] transition-all duration-300"
                  style={{
                    boxShadow: `0 0 0 0 ${step.glowColor}00`,
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLDivElement).style.boxShadow =
                      `0 0 25px ${step.glowColor}22`;
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLDivElement).style.boxShadow = "";
                  }}
                >
                  {/* Step number + icon */}
                  <div className="flex items-start justify-between">
                    <div
                      className="w-14 h-14 rounded-xl flex items-center justify-center"
                      style={{
                        background: `linear-gradient(135deg, ${step.glowColor}25, ${step.glowColor}08)`,
                        border: `1px solid ${step.glowColor}30`,
                      }}
                    >
                      <step.icon size={24} style={{ color: step.glowColor }} />
                    </div>
                    <span
                      className="text-4xl font-black opacity-15 font-mono"
                      style={{ color: step.glowColor }}
                    >
                      {step.number}
                    </span>
                  </div>

                  {/* Title */}
                  <div>
                    <h3 className="font-bold text-white text-lg leading-snug">{step.title}</h3>
                    <p className="text-xs text-slate-400 mt-0.5 tracking-wide">{step.subtitle}</p>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-slate-400 leading-relaxed flex-1">
                    {step.description}
                  </p>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-700/50">
                    {step.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 rounded-md text-[11px] font-medium"
                        style={{
                          background: `${step.glowColor}12`,
                          color: step.glowColor,
                          border: `1px solid ${step.glowColor}25`,
                        }}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Orchestrator callout */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-12 glass-card rounded-2xl p-6 flex flex-col md:flex-row items-center gap-6 text-center md:text-left"
        >
          <div className="flex-shrink-0 w-14 h-14 rounded-xl bg-teal/10 border border-teal/25 flex items-center justify-center">
            <Cpu size={26} className="text-teal" />
          </div>
          <div className="flex-1">
            <h4 className="font-bold text-white text-lg mb-1">EcoClawOrchestrator</h4>
            <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">
              The central coordinator chains all 4 agents sequentially with
              APScheduler cron jobs for 24/7 automated scans. It streams
              real-time progress back to the Telegram interface and persists
              results for human-in-the-loop review.
            </p>
          </div>
          <div className="flex-shrink-0 flex items-center gap-2 px-4 py-2 bg-teal/10 border border-teal/25 rounded-xl text-teal text-sm font-medium">
            <Database size={14} />
            OpenClaw Compatible
          </div>
        </motion.div>
      </div>
    </section>
  );
}
