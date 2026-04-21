#!/bin/bash

# SecureWealth Twin - Unified Startup Script

# Function to kill background processes on exit (Ctrl+C)
cleanup() {
    echo ""
    echo "Stopping background processes..."
    # Kill all background jobs started by this script
    kill $(jobs -p) 2>/dev/null
    exit
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM EXIT

echo "--------------------------------------"
echo "🚀 Starting SecureWealth Twin..."
echo "--------------------------------------"

# 1. Start Backend
echo "📡 Starting Backend (FastAPI) at http://0.0.0.0:8000..."
export PYTHONPATH=$PYTHONPATH:.
./venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait a moment for the backend to initialize
sleep 2

# 2. Start Frontend
echo "📱 Starting Frontend (Expo)..."
echo "Note: If you are running on a physical device, ensure your phone and computer are on the same Wi-Fi."
echo "--------------------------------------"
cd frontend && npx expo start
