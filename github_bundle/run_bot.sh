#!/bin/bash
set -e

cd "$(dirname "$0")"

# Ensure Python 3.11 exists (macOS Homebrew as fallback)
if ! command -v python3.11 >/dev/null 2>&1; then
  echo "Python 3.11 not found. Attempting Homebrew install..."
  if command -v brew >/dev/null 2>&1; then
    brew install python@3.11
  else
    echo "Homebrew not found. Please install Python 3.11 manually."
    exit 1
  fi
fi

# Create venv if missing
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment (.venv) with Python 3.11..."
  /opt/homebrew/opt/python@3.11/bin/python3.11 -m venv .venv 2>/dev/null || python3.11 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip & install requirements (if present)
python -m pip install --upgrade pip setuptools wheel
if [ -f "requirements.txt" ]; then
  python -m pip install -r requirements.txt
fi

# Ensure .env exists; prefer .env.example as source
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
  else
    # minimal default .env if example missing
    cat > .env <<'ENV'
SYMBOL=BTCUSDT
INTERVAL=1m
LOOKBACK=300
PAPER_STARTING_USDT=10000
PAPER_FEE_RATE=0.001
PAPER_SLIPPAGE_BPS=5
FAST_EMA=9
SLOW_EMA=21
POSITION_SIZE_USDT=250
LIVE_TRADING=false
BINANCE_API_KEY=
BINANCE_API_SECRET=
BINANCE_BASE_URL=https://api.binance.us
ENV
  fi
fi

# Force Binance.US endpoint for US users
if command -v sed >/dev/null 2>&1; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's#https://api.binance.com#https://api.binance.us#g' .env || true
  else
    sed -i 's#https://api.binance.com#https://api.binance.us#g' .env || true
  fi
fi

echo "✅ Environment ready. Launching API at http://localhost:8010/docs"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
