"use client";

import { motion } from "framer-motion";
import {
  Satellite,
  BarChart2,
  Brain,
  Link2,
  Shield,
  Users,
  Zap,
  ArrowRight,
} from "lucide-react";

const features = [
  {
    icon: Satellite,
    title: "Real-Time NASA & ESA Data",
    description:
      "FetcherAgent polls NASA EONET natural events feed and ESA Sentinel APIs every cycle, providing live coverage of floods, wildfires, droughts and deforestation worldwide.",
    tag: "Live Data",
    color: "#00D4FF",
  },
  {
    icon: BarChart2,
    title: "NDVI Change Detection",
    description:
      "AnalyzerAgent computes Normalized Difference Vegetation Index deltas using NumPy, overlays pixel-change heatmaps and exports Matplotlib charts directly to the chat interface.",
    tag: "Compression Co.",
    color: "#2A7A55",
  },
  {
    icon: Brain,
    title: "FLock & Z.AI Reasoning",
    description:
      "PredictorAgent chains FLock.io's federated climate LLM with Z.AI compound reasoning to generate detailed impact forecasts with confidence scores and recommended actions.",
    tag: "Federated AI",
    color: "#6366F1",
  },
  {
    icon: Link2,
    title: "On-Chain Alerts & NFT Rewards",
    description:
      "Web3CoordinatorAgent broadcasts verified alerts to Base chain, mints Animoca ERC-721 NFTs as contributor rewards and stores evidence CIDs permanently on Unibase.",
    tag: "Web3",
    color: "#EC4899",
  },
  {
    icon: Shield,
    title: "Permanent Storage",
    description:
      "Every analysis payload — satellite metadata, NDVI charts, prediction reports — is pinned to Unibase decentralised storage, generating immutable IPFS CIDs as proof-of-work.",
    tag: "Unibase IPFS",
    color: "#10B981",
  },
  {
    icon: Users,
    title: "Human-in-the-Loop Control",
    description:
      "Telegram inline keyboards let domain experts approve high-stakes agent actions before execution. Users rate predictions with 👍/👎 to steer future agent behaviour.",
    tag: "Imperial Blockchain",
    color: "#F59E0B",
  },
];

export default function Features() {
  return (
    <section id="features" className="py-24 px-6 bg-navy circuit-bg">
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
            Capabilities
          </span>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Everything You Need to{" "}
            <span className="gradient-text">Fight Climate Change</span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto text-lg">
            Six core capabilities working together — from raw pixels to
            on-chain proof — with zero manual intervention required.
          </p>
        </motion.div>

        {/* 3-column grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              whileHover={{ y: -4 }}
              className="group glass-card rounded-2xl p-6 flex flex-col gap-4 cursor-default relative overflow-hidden"
            >
              {/* Top accent bar on hover */}
              <div
                className="absolute top-0 left-0 right-0 h-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-t-2xl"
                style={{ background: f.color }}
              />

              {/* Icon + tag */}
              <div className="flex items-start justify-between">
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
                  style={{
                    background: `${f.color}18`,
                    border: `1px solid ${f.color}30`,
                  }}
                >
                  <f.icon size={22} style={{ color: f.color }} />
                </div>
                <span
                  className="text-xs px-2.5 py-1 rounded-full font-medium"
                  style={{
                    background: `${f.color}12`,
                    color: f.color,
                    border: `1px solid ${f.color}25`,
                  }}
                >
                  {f.tag}
                </span>
              </div>

              {/* Content */}
              <div>
                <h3 className="font-bold text-white text-lg mb-2 leading-snug">{f.title}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{f.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.6 }}
        className="mt-16 flex flex-col items-center gap-6"
      >
        <div className="h-px w-24 bg-teal/20" />
        <a
          href="https://t.me/ecoclawedbot"
          target="_blank"
          rel="noopener noreferrer"
          className="group flex items-center gap-3 px-8 py-4 rounded-2xl bg-navy-light border border-teal/20 hover:border-teal/50 hover:bg-navy-light/80 transition-all duration-300 shadow-xl shadow-teal/5"
        >
          <div className="w-10 h-10 rounded-xl bg-teal/10 flex items-center justify-center group-hover:bg-teal/20 transition-colors">
            <Zap size={20} className="text-teal" fill="currentColor" />
          </div>
          <div className="text-left">
            <div className="text-xs text-teal font-bold uppercase tracking-widest mb-0.5">Ready to Test?</div>
            <div className="text-white font-bold text-lg">Try These Features on Telegram</div>
          </div>
          <ArrowRight size={20} className="text-teal group-hover:translate-x-1 transition-transform ml-4" />
        </a>
      </motion.div>
    </section>
  );
}
