#!/bin/bash

echo "=== STARTING BACKEND SERVICES ==="

# Navigate to backend directory
cd backend

# Activate virtual environment
echo "1. Activating virtual environment..."
source venv/bin/activate

# Start scraping service
echo "2. Starting scraping service..."
cd scraping_service
uvicorn main:app --port 8001 --reload --host 0.0.0.0 > ../../scraping.log 2>&1 &
SCRAPING_PID=$!

# Start main API server
echo "3. Starting main API server..."
cd ../api
uvicorn master_server:app --reload --host 0.0.0.0 > ../../main.log 2>&1 &
API_PID=$!

# Wait for services to start
echo "4. Waiting for services to start..."
sleep 5

# Check service status
echo "5. Checking service status..."
echo "Main API:" && curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/docs && echo " - Running"
echo "Scraping API:" && curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001/docs && echo " - Running"

echo ""
echo "✅ Backend services started successfully!"
echo "🌐 Access points:"
echo "   • Main API: http://127.0.0.1:8000"
echo "   • API Docs: http://127.0.0.1:8000/docs"
echo "   • Scraping API: http://127.0.0.1:8001"
echo ""
echo "📝 Logs:"
echo "   • Main API: main.log"
echo "   • Scraping: scraping.log"
echo ""
echo "🛑 To stop services: pkill -f uvicorn" 