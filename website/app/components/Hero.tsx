"use client";

import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Github, Zap } from "lucide-react";
import Image from "next/image";

/* ─── Animated NDVI Canvas background ──────────────────────────────────── */
function NdviCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let t = 0;

    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    const draw = () => {
      const { width, height } = canvas;
      ctx.clearRect(0, 0, width, height);

      // Draw multiple NDVI-style waveforms
      const waves = [
        { color: "#00D4FF", alpha: 0.18, freq: 0.008, amp: 0.12, speed: 0.4, offset: 0 },
        { color: "#2A7A55", alpha: 0.14, freq: 0.012, amp: 0.09, speed: 0.6, offset: 1.5 },
        { color: "#00D4FF", alpha: 0.08, freq: 0.005, amp: 0.18, speed: 0.25, offset: 3 },
        { color: "#1E5B3F", alpha: 0.1,  freq: 0.018, amp: 0.06, speed: 0.8, offset: 0.8 },
      ];

      waves.forEach(({ color, alpha, freq, amp, speed, offset }) => {
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.globalAlpha = alpha;
        ctx.lineWidth = 1.5;

        for (let x = 0; x <= width; x += 2) {
          const y =
            height / 2 +
            Math.sin(x * freq + t * speed + offset) * height * amp +
            Math.sin(x * freq * 2.3 + t * speed * 0.7 + offset * 1.3) * height * amp * 0.4;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      });

      // Animated data points
      ctx.globalAlpha = 0.5;
      for (let i = 0; i < 6; i++) {
        const x = ((t * 80 + i * 180) % (width + 40)) - 20;
        const y =
          height / 2 +
          Math.sin(x * 0.008 + t * 0.4) * height * 0.12;
        ctx.beginPath();
        ctx.arc(x, y, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = "#00D4FF";
        ctx.fill();
      }

      ctx.globalAlpha = 1;
      t += 0.012;
      animId = requestAnimationFrame(draw);
    };

    draw();
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full opacity-60 pointer-events-none"
    />
  );
}

/* ─── Floating badge ────────────────────────────────────────────────────── */
function Badge({ children }: { children: React.ReactNode }) {
  return (
    <motion.span
      initial={{ opacity: 0, scale: 0.85 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-medium tracking-wide
        bg-teal/10 border border-teal/25 text-teal mb-6"
    >
      {children}
    </motion.span>
  );
}

/* ─── Hero ──────────────────────────────────────────────────────────────── */
export default function Hero() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden circuit-bg pt-24 pb-16">
      {/* Canvas bg */}
      <NdviCanvas />

      {/* Soft vignette at bottom only */}
      <div className="absolute bottom-0 left-0 right-0 h-48 bg-navy opacity-60 pointer-events-none" />

      <div className="relative z-10 text-center max-w-4xl mx-auto px-6">
        {/* Badge */}
        <Badge>
          <span className="w-1.5 h-1.5 rounded-full bg-teal animate-pulse" />
          UK AI Agent Hackathon EP4 × OpenClaw · March 2026
        </Badge>

        {/* Main logo / icon */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mb-8 flex items-center justify-center"
        >
          <div className="relative animate-float">
            <div className="absolute -inset-8 rounded-full bg-teal/20 blur-3xl opacity-50" />
            <div className="relative w-28 h-28 md:w-32 md:h-32 p-4 bg-navy-light/40 border border-teal/20 rounded-3xl backdrop-blur-sm flex items-center justify-center">
              <Image src="/logo.png" alt="EcoClaw" width={100} height={100} className="w-full h-full object-contain filter drop-shadow-[0_0_15px_rgba(45,212,191,0.3)]" />
            </div>
          </div>
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          className="text-4xl md:text-6xl lg:text-7xl font-extrabold leading-tight mb-6 tracking-tight"
        >
          Autonomous Climate Agents{" "}
          <span className="text-teal">That Actually Act</span>
        </motion.h1>

        {/* Sub-headline */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.55 }}
          className="text-lg md:text-xl text-slate-300 max-w-2xl mx-auto mb-10 leading-relaxed"
        >
          Satellite-powered multi-agent swarm that detects environmental threats,
          predicts impacts, posts on-chain alerts and mints NFT rewards — all in
          real time. Built on{" "}
          <span className="text-teal font-medium">OpenClaw</span>.
        </motion.p>

        {/* Branded URL pill */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.63 }}
          className="flex justify-center mb-8"
        >
          <a
            href="https://ecoclaw.vercel.app"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full
              bg-navy-light border border-teal/30 text-slate-300 hover:text-teal
              text-sm font-mono tracking-wide transition-colors duration-200 group"
          >
            <span className="w-2 h-2 rounded-full bg-teal animate-pulse flex-shrink-0" />
            <span>ecoclaw</span>
            <span className="text-teal font-bold">.vercel.app</span>
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="opacity-50 group-hover:opacity-100 transition-opacity">
              <path d="M2.5 9.5L9.5 2.5M9.5 2.5H4.5M9.5 2.5V7.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
        </motion.div>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.7 }}
          className="flex flex-col sm:flex-row gap-4 justify-center"
        >
          <a
            href="https://t.me/ecoclaw_bot"
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl
              text-navy-dark font-semibold bg-teal hover:bg-teal-dim
              glow-teal transition-all duration-200 hover:scale-105 text-base"
          >
            <Zap size={18} fill="currentColor" />
            Try Live Demo
            <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </a>
          <a
            href="https://github.com/0xshobha/ecoclaw"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl
              text-white font-semibold border border-slate-600 hover:border-teal/50
              bg-navy-light/50 hover:bg-navy-light transition-all duration-200 text-base"
          >
            <Github size={18} />
            View GitHub
          </a>
        </motion.div>

        {/* Stats row */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 1.0 }}
          className="mt-16 flex flex-wrap justify-center gap-8 md:gap-16"
        >
          {[
            { value: "7+", label: "Sponsor Integrations" },
            { value: "$10k+", label: "Bounties Targeted" },
            { value: "4", label: "Specialized Agents" },
            { value: "Real-time", label: "NASA Satellite Data" },
          ].map(({ value, label }) => (
            <div key={label} className="text-center">
              <div className="text-2xl md:text-3xl font-bold text-teal">{value}</div>
              <div className="text-xs text-slate-400 mt-1 tracking-wide">{label}</div>
            </div>
          ))}
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.5 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2"
      >
        <span className="text-xs text-slate-500 tracking-widest uppercase">Scroll</span>
        <div className="w-px h-8 bg-teal/30" />
      </motion.div>
    </section>
  );
}
