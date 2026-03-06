FROM python:3.12-slim

# ── System dependencies for OpenCV ───────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
  libgl1-mesa-glx \
  libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies (cached layer) ───────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project source ───────────────────────────────────────────────────────
COPY . .

# ── Create runtime directories ────────────────────────────────────────────────
RUN mkdir -p data logs

# ── Environment ───────────────────────────────────────────────────────────────
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# ── Default: start the Telegram bot ──────────────────────────────────────────
CMD ["python", "main.py"]
