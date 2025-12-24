#!/bin/bash
# Helper script to view backend logs in real-time

cd "$(dirname "$0")/backend"

if [ ! -f backend.log ]; then
    echo "⚠️  Log file not found. Make sure the backend is running."
    echo "   The log file will be created at: $(pwd)/backend.log"
    exit 1
fi

echo "📋 Viewing backend logs (Ctrl+C to stop)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -f backend.log
