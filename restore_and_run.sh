#!/bin/bash
set -e

# Step 1: Create .env from example if missing
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        sed -i '' 's#https://api.binance.com#https://api.binance.us#g' .env
        echo "✅ Created .env from .env.example and set Binance.US endpoint"
    else
        echo "❌ No .env.example found!"
        exit 1
    fi
else
    echo "ℹ️ .env already exists"
fi

# Step 2: Create and activate virtual environment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Created new virtual environment"
fi
source .venv/bin/activate
echo "✅ Virtual environment activated"

# Step 3: Install dependencies
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Step 4: Run the bot API
echo "🚀 Starting Binance Bot..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8010

