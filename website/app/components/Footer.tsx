"use client";

import { Github, ExternalLink, Send, Heart, Leaf } from "lucide-react";

const footerLinks: Record<string, { label: string; href: string; external: boolean }[]> = {
  Product: [
    { label: "How It Works", href: "#how-it-works", external: false },
    { label: "Integrations", href: "#integrations", external: false },
    { label: "Features", href: "#features", external: false },
    { label: "Live Demo", href: "#demo", external: false },
  ],
  Resources: [
    { label: "GitHub Repository", href: "https://github.com/your-org/ecoclaw", external: true },
    { label: "Documentation", href: "https://github.com/your-org/ecoclaw#readme", external: true },
    { label: "DoraHacks Submission", href: "https://dorahacks.io", external: true },
    { label: "OpenClaw Docs", href: "https://openclaw.io/docs", external: true },
  ],
  Sponsors: [
    { label: "FLock.io", href: "https://flock.io", external: true },
    { label: "Z.AI", href: "https://z.ai", external: true },
    { label: "Animoca Brands", href: "https://animocabrands.com", external: true },
    { label: "Virtual Protocol", href: "#", external: false },
  ],
};

export default function Footer() {
  return (
    <footer className="bg-navy-dark border-t border-teal/8 pt-16 pb-8 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Top section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 mb-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 rounded-xl bg-teal/15 border border-teal/25 flex items-center justify-center text-xl">
                🌍
              </div>
              <span className="font-bold text-xl">
                <span className="text-white">Eco</span>
                <span className="gradient-text-teal">Claw</span>
              </span>
            </div>
            <p className="text-slate-400 text-sm leading-relaxed mb-5 max-w-xs">
              Autonomous climate agents that detect, predict and act — powered by
              satellite data, federated AI and Web3 incentives.
            </p>
            <div className="flex items-center gap-3">
              <a
                href="https://github.com/your-org/ecoclaw"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-3 py-2 rounded-lg border border-slate-700 hover:border-teal/40 text-slate-400 hover:text-white text-sm transition-all"
              >
                <Github size={15} />
                GitHub
              </a>
              <a
                href="https://t.me/your_ecoclaw_bot"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-3 py-2 rounded-lg bg-teal/15 border border-teal/25 text-teal hover:bg-teal/25 text-sm transition-all"
              >
                <Send size={15} />
                Telegram Bot
              </a>
            </div>
          </div>

          {/* Links */}
          {Object.entries(footerLinks).map(([section, links]) => (
            <div key={section}>
              <h4 className="font-semibold text-white text-sm mb-4 tracking-wide">{section}</h4>
              <ul className="space-y-2.5">
                {links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      {...(link.external
                        ? { target: "_blank", rel: "noopener noreferrer" }
                        : {})}
                      className="flex items-center gap-1.5 text-sm text-slate-400 hover:text-teal transition-colors group"
                    >
                      {link.label}
                      {link.external && (
                        <ExternalLink
                          size={10}
                          className="opacity-0 group-hover:opacity-100 transition-opacity"
                        />
                      )}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Divider */}
        <div className="h-px bg-teal/12 mb-8" />

        {/* Bottom bar */}
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-slate-500">
          <div className="flex items-center gap-2">
            <Leaf size={14} className="text-forest-light" />
            <span>
              Made with{" "}
              <Heart size={12} className="inline text-red-400" fill="currentColor" />{" "}
              for the planet · EcoClaw 2026
            </span>
          </div>

          <div className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-teal animate-pulse" />
            <span>UK AI Agent Hackathon EP4 × OpenClaw</span>
          </div>

          <div>
            <span>MIT License · Open Source</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
