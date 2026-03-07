"use client";

import { motion, Variants } from "framer-motion";
import {
  AlertTriangle,
  Clock,
  Eye,
  Users,
  Globe,
  ShieldCheck,
  TrendingUp,
  Zap,
  ArrowRight,
} from "lucide-react";

const problems = [
  {
    icon: Clock,
    title: "Slow Detection",
    description:
      "Traditional climate monitoring takes days or weeks. Deforestation events, floods and wildfires spread unchecked while data is still being processed.",
  },
  {
    icon: Eye,
    title: "Fragmented Analysis",
    description:
      "Satellite data, weather feeds and ground reports live in silos. No single system correlates them into actionable intelligence automatically.",
  },
  {
    icon: Users,
    title: "No Community Incentive",
    description:
      "Volunteers who submit ground-truth data get nothing in return, leading to sparse coverage in critical regions.",
  },
  {
    icon: AlertTriangle,
    title: "Expertise Barrier",
    description:
      "Researchers and NGOs lack the ML engineering skills to build autonomous analysis pipelines — so threats go undetected.",
  },
];

const solutions = [
  {
    icon: Zap,
    title: "Real-Time Agent Swarm",
    description:
      "EcoClaw deploys 4 specialized AI agents 24/7 — fetching live NASA/ESA data, running NDVI analysis, predicting impacts, and triggering on-chain actions automatically.",
    border: "border-teal/25",
  },
  {
    icon: Globe,
    title: "Unified Intelligence Layer",
    description:
      "FLock federated LLMs and Z.AI compound reasoning fuse satellite imagery, weather data and historical trends into a single, actionable risk score.",
    border: "border-forest-light/30",
  },
  {
    icon: ShieldCheck,
    title: "Web3 Reward Engine",
    description:
      "Animoca NFTs reward verified contributors. Unibase stores permanent proof on-chain. Virtual Protocol registers every agent action for full auditability.",
    border: "border-teal/20",
  },
  {
    icon: TrendingUp,
    title: "Human-in-the-Loop",
    description:
      "Telegram interface lets domain experts approve high-risk agent actions, rate predictions and steer agent behaviour — zero code required.",
    border: "border-forest-light/25",
  },
];

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: i * 0.1, ease: [0.25, 0.46, 0.45, 0.94] },
  }),
};

export default function ProblemSolution() {
  return (
    <section id="problem" className="py-24 px-6 bg-navy-dark circuit-bg">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <span className="inline-block px-3 py-1 text-xs font-medium tracking-widest uppercase text-teal bg-teal/10 rounded-full border border-teal/20 mb-4">
            The Challenge
          </span>
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Climate Crisis Needs{" "}
            <span className="gradient-text">Faster Intelligence</span>
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto text-lg">
            Every hour of delay in detecting environmental threats means more
            irreversible damage. We built EcoClaw to close the gap.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-12 md:gap-20">
          {/* Problem column */}
          <div>
            <motion.h3
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="flex items-center gap-3 text-xl font-bold mb-8 text-red-400"
            >
              <span className="flex-shrink-0 w-8 h-8 rounded-full bg-red-500/20 border border-red-500/30 flex items-center justify-center">
                <AlertTriangle size={15} className="text-red-400" />
              </span>
              The Problem
            </motion.h3>

            <div className="space-y-5">
              {problems.map((item, i) => (
                <motion.div
                  key={item.title}
                  custom={i}
                  variants={fadeUp}
                  initial="hidden"
                  whileInView="visible"
                  viewport={{ once: true }}
                  className="glass-card rounded-xl p-5 flex gap-4 hover:border-red-500/20 transition-colors"
                >
                  <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center justify-center mt-0.5">
                    <item.icon size={18} className="text-red-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-1">{item.title}</h4>
                    <p className="text-sm text-slate-400 leading-relaxed">{item.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Solution column */}
          <div>
            <motion.h3
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="flex items-center gap-3 text-xl font-bold mb-8 text-teal"
            >
              <span className="flex-shrink-0 w-8 h-8 rounded-full bg-teal/20 border border-teal/30 flex items-center justify-center">
                <Zap size={15} className="text-teal" fill="currentColor" />
              </span>
              EcoClaw&apos;s Solution
            </motion.h3>

            <div className="space-y-5">
              {solutions.map((item, i) => (
                <motion.div
                  key={item.title}
                  custom={i}
                  variants={fadeUp}
                  initial="hidden"
                  whileInView="visible"
                  viewport={{ once: true }}
                  className={`glass-card rounded-xl p-5 flex gap-4 border ${item.border} hover:scale-[1.01] transition-transform`}
                >
                  <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-teal/15 border border-teal/25 flex items-center justify-center mt-0.5">
                    <item.icon size={18} className="text-teal" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-1">{item.title}</h4>
                    <p className="text-sm text-slate-400 leading-relaxed">{item.description}</p>
                  </div>
                </motion.div>
              ))}

              <motion.div
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.5, duration: 0.5 }}
                className="mt-8"
              >
                <a
                  href="https://t.me/ecoclawedbot"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-xl
                  bg-teal/10 border border-teal/25 text-teal hover:bg-teal/20 transition-all duration-300"
                >
                  <Zap size={18} fill="currentColor" />
                  <span className="font-bold">Test the Solution in Telegram</span>
                  <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                </a>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
