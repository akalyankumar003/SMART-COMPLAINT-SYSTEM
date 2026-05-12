#!/bin/bash

echo "═══════════════════════════════════════════════════════"
echo "🚀 STARTING SMART COMPLAINT SYSTEM"
echo "═══════════════════════════════════════════════════════"
echo ""



# Initialize database (only first time)
if [ "$1" == "--init" ]; then
    echo "📦 Initializing database..."
    python init_db.py
    echo ""
    
    echo "🌱 Seeding database..."
    python seed.py
    echo ""
fi

# Start Flask server
echo "🔥 Starting Flask server..."
python app.py
