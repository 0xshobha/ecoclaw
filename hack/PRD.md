# Product Requirements Document (PRD): EcoClaw MVP

## Version History
- **Version**: 1.0
- **Date**: March 05, 2026
- **Author**: Grok (AI Assistant for UK AI Agent Hackathon EP4)
- **Status**: Draft for MVP Build
- **Purpose**: This PRD outlines the requirements for building a minimum viable product (MVP) of EcoClaw, an AI multi-agent network focused on climate "for good" applications. Designed to maximize bounties in the UK AI Agent Hackathon EP4 x OpenClaw (e.g., FLock.io's $5k "AI Agents for Good", Compression Company's $1k GBP "AI Agent for Satellite Imagery Analytics", Z.AI's $4k General, Animoca Brands' $1k, Imperial Blockchain's $500 "Claw for Human" and $500 "Human for Claw", BGA's Blockchain for Good, and potentially others like Virtual Protocol or Unibase for Web3 integrations).
- **Timeline**: Build and submit MVP by March 08, 2026 (3 days from now). Prioritize core functionality for live demo.

## Executive Summary
EcoClaw is a production-ready multi-agent system built on OpenClaw, enabling autonomous AI agents to monitor, analyze, and act on climate-related data. The MVP focuses on real-world integrations: scraping/analyzing satellite imagery for environmental threats (e.g., deforestation, floods), predictive modeling, on-chain data crowdsourcing/rewards, and human-in-the-loop interactions via chat interfaces.

**Key Value Proposition**:
- Empowers users (e.g., researchers, activists) to deploy agents that detect climate issues in real-time, coordinate responses, and incentivize community participation via Web3.
- "Agents for Good" theme aligns with sponsor bounties by using live APIs, SDKs, and protocols for impactful, deployable systems.
- MVP Goal: A live Telegram/Slack bot where users query agents, which process real data and output actionable insights/alerts.

**Target Users**: Hackathon participants (builders), end-users (climate enthusiasts, NGOs), judges (sponsors/VCs evaluating integrations).

**Success Metrics for MVP**:
- Deployable on a VPS with always-on agents.
- Successful integration of 5+ sponsors (e.g., FLock for models, Compression for imagery, Animoca for Web3).
- Live demo: Agent analyzes sample satellite data, predicts outcomes, and posts on-chain alert.
- Bounty Claims: Aim for 7+ by tagging integrations in DoraHacks submission.

**Assumptions & Constraints**:
- Team: 2-4 builders (1 OpenClaw expert, 1 integrator, 1 tester/demo).
- Time: 3 days – Day 1: Setup & Core; Day 2: Integrations; Day 3: Polish & Submit.
- Resources: Free OpenAI Codex credits, sponsor API access (request via Discord/X).
- No custom hardware; use cloud (e.g., free AWS/GCP tiers).

## Problem Statement
Climate monitoring relies on manual analysis of vast data sources (e.g., satellite imagery, public datasets). Challenges include:
- Slow detection of events like deforestation or floods.
- Lack of coordination between data analysis, prediction, and community action.
- Limited accessibility for non-experts.

EcoClaw solves this with autonomous multi-agents: One agent fetches/analyzes data, another predicts impacts, a third crowdsources via Web3, and all orchestrate via OpenClaw with human oversight.

## Goals & Objectives
- **Primary**: Build a working MVP that demonstrates multi-agent orchestration on OpenClaw with live sponsor integrations.
- **Secondary**: Maximize bounty eligibility by incorporating sponsor tools (e.g., FLock APIs for cost-effective LLMs, Compression SDK for imagery).
- **Non-Goals for MVP**: Full-scale production (e.g., no user auth, scalability to 1000s of users); advanced UI (stick to chat interfaces).

## Scope
**In Scope**:
- Core multi-agent system on OpenClaw.
- Integrations: 5-7 sponsors.
- Basic deployment and demo.
**Out of Scope**:
- Mobile app; advanced security (e.g., encryption).
- Extensive testing (focus on happy paths).

## Technical Stack
- **Core Framework**: OpenClaw (open-source agent toolkit; install via pip or GitHub fork).
- **Languages**: Python (primary for agents), JavaScript (if needed for Web3 frontends).
- **LLMs/Models**: FLock.io API (federated, cheap alternatives to OpenAI); Z.AI for compound AI reasoning.
- **Data Sources/APIs**:
  - Satellite Imagery: Compression Company SDK + free public APIs (e.g., NASA Earthdata via code_execution tool if needed for testing).
  - Web3: Animoca Brands (NFT rewards), Unibase/Virtual Protocol (on-chain storage), BGA for "good" blockchain.
- **Tools/Skills**: OpenClaw's built-ins (browser, file ops, cron for scheduling), custom skills for sponsors.
- **Deployment**: VPS (e.g., DigitalOcean droplet, $5/mo) for always-on; Telegram/Slack for user interface.
- **Dependencies**: Use code_execution env libs (numpy for analysis, rdkit if bio-tie-in, but focus on core).

## Features & Requirements
Features are prioritized as Must-Have (core MVP), Should-Have (bounty boosters), Nice-to-Have (if time).

### 1. Agent Orchestration (Must-Have)
- **Description**: Central OpenClaw instance manages a swarm of 3-4 specialized agents.
- **Requirements**:
  - Agent 1: Data Fetcher – Scrapes satellite imagery URLs (e.g., via browser tool) and downloads samples.
  - Agent 2: Analyzer – Processes images (e.g., detect changes using numpy/OpenCV if available in env).
  - Agent 3: Predictor – Uses FLock/Z.AI models to forecast impacts (e.g., "Flood risk: High").
  - Agent 4: Web3 Coordinator – Posts alerts to blockchain (e.g., mint NFT reward via Animoca).
  - Orchestration: Agents communicate via OpenClaw's cron/jobs; trigger workflows (e.g., daily scans).
- **Integrations**: OpenClaw backbone + Z.AI for reasoning.

### 2. Satellite Imagery Analytics (Must-Have for Compression Bounty)
- **Description**: Agent analyzes real satellite data for environmental insights.
- **Requirements**:
  - Input: User queries "Analyze deforestation in Amazon" via chat.
  - Process: Fetch free NASA/ESA imagery (use browse_page tool if needed for URLs); apply basic analytics (e.g., pixel change detection).
  - Output: Report with insights (e.g., "10% deforestation detected") + visual (if env allows matplotlib plots).
- **Integrations**: Compression Company SDK (request access); fallback to public APIs.

### 3. "For Good" Web3 Incentives (Should-Have for FLock, Animoca, BGA Bounties)
- **Description**: Agents crowdsource data/reports via blockchain rewards.
- **Requirements**:
  - On-chain Action: Agent mints/shares NFT (Animoca) for user contributions (e.g., verify ground-truth photos).
  - Good Focus: Tie to climate (e.g., carbon offset simulations).
  - Output: Transaction hash in chat response.
- **Integrations**: Animoca SDK, BGA protocols, Virtual Protocol for agent NFTs.

### 4. Human-in-the-Loop Interactions (Should-Have for Imperial Bounties)
- **Description**: "Claw for Human" (agents assist users) and "Human for Claw" (users refine agents).
- **Requirements**:
  - Chat Interface: Telegram bot where users approve actions (e.g., "Confirm alert post?").
  - Feedback Loop: Users rate predictions, agents learn (basic via persistent state).
- **Integrations**: OpenClaw channels + Imperial Blockchain tools.

### 5. Deployment & Monitoring (Must-Have)
- **Description**: Always-on system with basic logging.
- **Requirements**:
  - Deploy: Dockerize OpenClaw + agents; run on VPS.
  - Demo: 5-min video showing end-to-end (query → analysis → on-chain alert).
  - Logging: Simple prints/errors to file.

## User Stories
- As a user, I can message the bot "Scan for floods in UK" so the agents fetch/analyze satellite data and reply with predictions.
- As a builder, I can extend agents with custom skills to integrate new sponsors without breaking core.
- As a judge, I can see live interactions with real infra (e.g., FLock API calls) in the demo.

## Design Considerations
- **Architecture**: Modular – Each agent as OpenClaw plugin/module.
- **UI/UX**: Text-based (chat); no fancy frontend.
- **Data Flow**: User Query → OpenClaw Router → Agent Swarm → Response.
- **Error Handling**: Graceful fallbacks (e.g., mock data if API fails).
- **Security**: Basic – No sensitive data; use env vars for API keys.

## Risks & Mitigations
- **Risk**: API Access Delays – Mitigation: Request early via X/Discord; use mocks.
- **Risk**: Time Crunch – Mitigation: Focus on 3 agents first, add more iteratively.
- **Risk**: Env Limits – Mitigation: Test code in code_execution tool if needed (e.g., for numpy analytics).

## Development Plan
- **Day 1 (March 05)**: Fork OpenClaw, setup core agents, integrate FLock/Z.AI.
- **Day 2 (March 06)**: Add Compression imagery + Web3 (Animoca).
- **Day 3 (March 07)**: Human loops, deploy, record demo, submit to DoraHacks with bounty tags.
- **Testing**: Manual – Run 5 queries; check integrations.

## Appendix
- **Resources**: OpenClaw Docs (browse_page if needed: url="https://openclaw.io/docs", instructions="Summarize setup and custom skills"); Sponsor SDKs (search via web_search if unclear).
- **Next Steps**: If team needs code snippets, request in follow-up. Build fast – this MVP could net $10k+ in bounties!