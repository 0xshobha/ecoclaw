# EcoClaw 🌍

> **AI Multi-Agent Network for Climate Good**
> Built for **UK AI Agent Hackathon EP4 × OpenClaw** (March 2026)

EcoClaw is a production-ready, OpenClaw-compatible multi-agent system that autonomously monitors, analyses, and acts on real-time climate data — using satellite imagery, federated LLMs, compound AI reasoning, and on-chain Web3 incentives.

---

## Architecture

```
User (Telegram)
      │
      ▼
EcoClawOrchestrator
      │
      ├─► FetcherAgent       ← NASA EONET + Compression Company SDK
      │
      ├─► AnalyzerAgent      ← NumPy NDVI change-detection + risk scoring
      │
      ├─► PredictorAgent     ← FLock.io LLM + Z.AI compound reasoning
      │
      └─► Web3CoordinatorAgent  ← Animoca NFT + Unibase storage + Virtual Protocol
```

All agents implement the `BaseAgent` interface (OpenClaw-compatible). The orchestrator chains them sequentially with streaming progress callbacks sent back to the Telegram chat.

---

## Sponsor Integrations (Bounty Coverage)

| Sponsor                  | Bounty                   | Integration                                                              |
| ------------------------ | ------------------------ | ------------------------------------------------------------------------ |
| **FLock.io**             | $5k – AI Agents for Good | `skills/flock_llm.py` – federated climate LLM                            |
| **Z.AI**                 | $4k – General            | `skills/zai_llm.py` – compound AI reasoning                              |
| **Compression Company**  | £1k – Satellite Imagery  | `skills/satellite.py` – imagery analytics + NDVI charts                  |
| **Animoca Brands / BGA** | $1k – Web3               | `skills/animoca_web3.py` – Base-chain alert hashes + ERC-721 NFT rewards |
| **Unibase**              | On-chain storage         | `skills/unibase.py` – permanent decentralised payload storage (IPFS)     |
| **Virtual Protocol**     | Agent-NFT reputation     | `skills/virtual_protocol.py` – on-chain agent action registry            |
| **Imperial Blockchain**  | $500 – Claw for Human    | Telegram inline keyboard confirmation loop                               |
| **Imperial Blockchain**  | $500 – Human for Claw    | User feedback via `/status` + wallet registration                        |

---

## Quick Start

### 1 · Clone & configure

```bash
git clone https://github.com/0xshobha/ecoclaw
cd ecoclaw
cp .env.example .env
# Edit .env with your API keys
```

### 2 · Install dependencies

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3 · Run demo (no API keys needed – mock mode)

```bash
python main.py --demo
# Custom query:
python main.py --demo --query "scan for floods in uk"
```

### 4 · Start Telegram bot

```bash
# Add your TELEGRAM_TOKEN to .env first
python main.py
```

### 5 · Docker

```bash
docker compose up --build -d
docker compose logs -f
```

---

## Configuration (`.env`)

| Variable                    | Description                           | Default                      |
| --------------------------- | ------------------------------------- | ---------------------------- |
| `TELEGRAM_TOKEN`            | BotFather token                       | _required_                   |
| `FLOCK_API_KEY`             | FLock.io API key                      | _required for live_          |
| `ZAI_API_KEY`               | Z.AI API key                          | _required for live_          |
| `NASA_API_KEY`              | NASA Earthdata key (free)             | `DEMO_KEY`                   |
| `COMPRESSION_API_KEY`       | Compression Company SDK key           | _optional_                   |
| `UNIBASE_API_KEY`           | Unibase decentralised storage key     | _optional_                   |
| `VIRTUAL_PROTOCOL_API_KEY`  | Virtual Protocol agent-NFT key        | _optional_                   |
| `VIRTUAL_PROTOCOL_AGENT_ID` | Agent identifier on Virtual Protocol  | `ecoclaw-agent-v1`           |
| `WALLET_PRIVATE_KEY`        | EVM wallet for NFT minting            | _optional_                   |
| `WEBHOOK_URL`               | Public HTTPS URL for Telegram webhook | _optional (blank = polling)_ |
| `WEBHOOK_PORT`              | Webhook listen port                   | `8443`                       |
| `WEBHOOK_SECRET`            | Webhook secret token                  | _optional_                   |
| `MOCK_MODE`                 | `true` / `false`                      | `true`                       |

---

## Project Structure

```
ecoclaw/
├── config/          Settings & environment
├── agents/          BaseAgent + 4 specialised agents
├── skills/          External API wrappers (FLock, Z.AI, NASA, Animoca)
├── orchestrator/    Pipeline coordinator + APScheduler cron jobs
├── interfaces/      Telegram bot (human-in-the-loop)
├── utils/           Logging (loguru) + helper functions
├── data/            Cached satellite data (gitignored)
├── logs/            Rotating log files (gitignored)
├── Dockerfile
├── docker-compose.yml
└── main.py          Entry point
```

---

## Telegram Commands

| Command                      | Description                                                                  |
| ---------------------------- | ---------------------------------------------------------------------------- |
| `/scan amazon deforestation` | Run the full 4-agent pipeline via [@ecoclawedbot](https://t.me/ecoclawedbot) |
| `/status`                    | Last scan summary                                                            |
| `/register 0x…`              | Link wallet for NFT rewards                                                  |
| `/agents`                    | List loaded agents                                                           |
| `/help`                      | Welcome message                                                              |

Free-text climate queries (e.g. "scan for floods in UK") trigger a human-in-the-loop confirmation keyboard before agents are dispatched.

---

## Development

```bash
# Run a scheduled multi-region scan
python main.py --scan

# Run the full test suite (all offline, no API keys needed)
pytest tests/ -v

# Run only skills tests
pytest tests/test_skills.py -v
```

---

## Telegram Webhook Mode

By default the bot uses long-polling (no public URL required). To switch to webhook mode (needed for production VPS deployments):

```bash
# In .env:
WEBHOOK_URL=https://yourdomain.com   # must be publicly reachable HTTPS
WEBHOOK_PORT=8443
WEBHOOK_SECRET=some_random_secret_here
```

The bot will automatically detect `WEBHOOK_URL` and call `run_webhook()` instead of `run_polling()`.

---

## License

MIT – build freely, ship fast, save the planet. 🌱
