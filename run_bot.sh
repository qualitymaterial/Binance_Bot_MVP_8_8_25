#!/bin/bash
set -e

# Always make sure we're using Binance.US endpoint
if [ -f ".env" ]; then
    sed -i '' 's#https://api.binance.com#https://api.binance.us#g' .env
    echo "✅ Updated .env to use Binance.US"
elif [ -f ".env.example" ]; then
    cp .env.example .env
    sed -i '' 's#https://api.binance.com#https://api.binance.us#g' .env
    echo "✅ Created and updated .env to use Binance.US"
else
    echo "❌ No .env or .env.example found!"
    exit 1
fi

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run:"
    echo "python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Run the bot
echo "🚀 Starting Binance Bot..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
#!/bin/bash
set -e

# Change to script directory (project root)
cd "$(dirname "$0")"

# Install Python 3.11 if not found
if ! command -v python3.11 &>/dev/null; then
    echo "Installing Python 3.11 via Homebrew..."
    brew install python@3.11
fi

# Create venv if missing
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with Python 3.11..."
    /opt/homebrew/opt/python@3.11/bin/python3.11 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip + install requirements
echo "Upgrading pip and installing requirements..."
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

# Copy env file if missing
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from .env.example"
fi

# Run the bot
echo "Starting Binance Bot on port 8010..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8010
