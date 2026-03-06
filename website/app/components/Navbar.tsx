"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Github, ExternalLink, Menu, X, Zap } from "lucide-react";

const links = [
  { label: "How it Works", href: "#how-it-works" },
  { label: "Integrations", href: "#integrations" },
  { label: "Features", href: "#features" },
  { label: "Demo", href: "#demo" },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <motion.nav
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? "glass-nav py-3" : "py-5 bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        {/* Logo */}
        <a href="#" className="flex items-center gap-2.5 group">
          <div className="relative w-9 h-9 flex items-center justify-center">
            <div className="absolute inset-0 rounded-xl bg-teal/15 border border-teal/25 group-hover:bg-teal/25 transition-all duration-300" />
            <span className="relative text-xl leading-none select-none">🌍</span>
          </div>
          <span className="font-bold text-xl tracking-tight">
            <span className="text-white">Eco</span>
            <span className="text-teal">Claw</span>
          </span>
        </a>

        {/* Desktop Links */}
        <ul className="hidden md:flex items-center gap-1">
          {links.map((l) => (
            <li key={l.href}>
              <a
                href={l.href}
                className="relative px-4 py-2 text-sm text-slate-300 hover:text-white transition-colors group"
              >
                {l.label}
                <span className="absolute bottom-0 left-4 right-4 h-px bg-teal scale-x-0 group-hover:scale-x-100 transition-transform duration-200 origin-left" />
              </a>
            </li>
          ))}
        </ul>

        {/* Desktop CTAs */}
        <div className="hidden md:flex items-center gap-3">
          <a
            href="https://github.com/your-org/ecoclaw"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-slate-300 hover:text-white border border-slate-600 hover:border-slate-400 rounded-lg transition-all duration-200"
          >
            <Github size={15} />
            <span>Star on GitHub</span>
          </a>
          <a
            href="https://t.me/your_ecoclaw_bot"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 px-4 py-1.5 text-sm font-medium text-navy-dark bg-teal hover:bg-teal-dim rounded-lg transition-all duration-200 glow-teal-sm hover:scale-105"
          >
            <Zap size={14} fill="currentColor" />
            Launch Bot
          </a>
        </div>

        {/* Mobile toggle */}
        <button
          className="md:hidden text-slate-300 hover:text-white p-1"
          onClick={() => setMobileOpen((v) => !v)}
          aria-label="Toggle menu"
        >
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="md:hidden overflow-hidden glass-nav border-t border-teal/10"
          >
            <div className="px-6 py-4 flex flex-col gap-3">
              {links.map((l) => (
                <a
                  key={l.href}
                  href={l.href}
                  className="text-slate-300 hover:text-teal transition-colors py-1 text-sm"
                  onClick={() => setMobileOpen(false)}
                >
                  {l.label}
                </a>
              ))}
              <div className="pt-3 flex flex-col gap-2 border-t border-slate-700/50">
                <a
                  href="https://github.com/your-org/ecoclaw"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 text-sm text-slate-300 hover:text-white"
                >
                  <Github size={15} />
                  View GitHub
                  <ExternalLink size={12} />
                </a>
                <a
                  href="https://t.me/your_ecoclaw_bot"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 py-2 px-4 text-sm font-medium text-navy bg-teal rounded-lg"
                >
                  <Zap size={14} fill="currentColor" />
                  Launch Telegram Bot
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
}
