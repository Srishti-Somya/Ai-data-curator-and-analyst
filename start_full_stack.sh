#!/bin/bash

echo "=== STARTING FULL STACK APPLICATION ==="

# Stop any existing services
echo "1. Stopping existing services..."
pkill -f uvicorn 2>/dev/null || true
pkill -f "next dev" 2>/dev/null || true
sleep 3

# Start backend services
echo "2. Starting backend services..."
./start_backend.sh

# Wait a moment
sleep 3

# Start frontend
echo "3. Starting frontend..."
./start_frontend.sh

# Final status check
echo "4. Final status check..."
sleep 5
echo "Frontend:" && curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 && echo " - Running"
echo "Main API:" && curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/docs && echo " - Running"
echo "Scraping API:" && curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001/docs && echo " - Running"

echo ""
echo "🎉 FULL STACK APPLICATION STARTED!"
echo "=================================="
echo ""
echo "🌐 Access Points:"
echo "   • Frontend: http://localhost:3000"
echo "   • Main API: http://127.0.0.1:8000"
echo "   • API Docs: http://127.0.0.1:8000/docs"
echo "   • Scraping API: http://127.0.0.1:8001"
echo ""
echo "📝 Logs:"
echo "   • Frontend: frontend.log"
echo "   • Main API: main.log"
echo "   • Scraping: scraping.log"
echo ""
echo "🛑 To stop all services:"
echo "   pkill -f uvicorn && pkill -f 'next dev'"
echo ""
echo "🚀 Ready to use! Open http://localhost:3000" 