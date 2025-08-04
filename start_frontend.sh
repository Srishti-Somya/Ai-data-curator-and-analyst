#!/bin/bash

echo "=== STARTING FRONTEND ==="

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "1. Installing dependencies..."
    npm install
fi

# Start frontend
echo "2. Starting frontend..."
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo "3. Waiting for frontend to start..."
sleep 8

# Check frontend status
echo "4. Checking frontend status..."
echo "Frontend:" && curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 && echo " - Running"

echo ""
echo "✅ Frontend started successfully!"
echo "🌐 Access point: http://localhost:3000"
echo ""
echo "📝 Logs: frontend.log"
echo ""
echo "🛑 To stop frontend: pkill -f 'next dev'" 