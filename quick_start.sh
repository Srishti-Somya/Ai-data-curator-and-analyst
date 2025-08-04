#!/bin/bash

# AI Tool for Data Curation and Analysis - Quick Start Script

echo "🚀 Starting AI Tool for Data Curation and Analysis..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "Server/master_server.py" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Kill any existing uvicorn processes
print_status "Stopping any existing servers..."
pkill -f uvicorn 2>/dev/null
sleep 2

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi, uvicorn, selenium, beautifulsoup4, spacy, pandas, httpx" 2>/dev/null; then
    print_status "Installing dependencies..."
    pip install fastapi uvicorn selenium beautifulsoup4 spacy pandas httpx
    print_success "Dependencies installed"
fi

# Check if spaCy models are installed
if ! python -c "import spacy; spacy.load('en_core_web_lg')" 2>/dev/null; then
    print_status "Downloading spaCy models..."
    python -m spacy download en_core_web_lg
    python -m spacy download en_core_web_sm
    print_success "spaCy models downloaded"
fi

# Create scraped_data directory if it doesn't exist
mkdir -p Server/scraped_data

# Start scraping service in background
print_status "Starting scraping service on port 8001..."
cd Server/Scrapping_modules_init
uvicorn main:app --port 8001 --reload --log-level info > ../../scraping_service.log 2>&1 &
SCRAPING_PID=$!
cd ../..

# Wait a moment for scraping service to start
sleep 3

# Start main server in background
print_status "Starting main server on port 8000..."
cd Server
uvicorn master_server:app --reload --log-level info > ../main_server.log 2>&1 &
MAIN_PID=$!
cd ..

# Wait for servers to start
sleep 5

# Check if servers are running
if curl -s http://127.0.0.1:8001/docs > /dev/null; then
    print_success "Scraping service is running on http://127.0.0.1:8001"
else
    print_error "Scraping service failed to start"
    exit 1
fi

if curl -s http://127.0.0.1:8000/docs > /dev/null; then
    print_success "Main server is running on http://127.0.0.1:8000"
else
    print_error "Main server failed to start"
    exit 1
fi

print_success "🎉 All services are running successfully!"

echo ""
echo "📋 Available endpoints:"
echo "   Main API: http://127.0.0.1:8000"
echo "   Scraping API: http://127.0.0.1:8001"
echo "   Interactive Docs: http://127.0.0.1:8000/docs"
echo ""

echo "🧪 Quick test query:"
echo "curl -X POST http://127.0.0.1:8000/process \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"query\": \"artificial intelligence trends 2024\", \"keywords\": [\"AI\", \"machine learning\"], \"columns_to_save\": [\"Person\", \"Org\", \"Date\", \"Loc\"]}'"
echo ""

echo "📁 Generated files will be in:"
echo "   Scraped data: Server/scraped_data/"
echo "   CSV output: Server/structured_data.csv"
echo "   SVG visualization: Server/relationships.svg"
echo ""

echo "🛑 To stop the servers, run:"
echo "   pkill -f uvicorn"
echo ""

# Function to handle script termination
cleanup() {
    print_status "Stopping servers..."
    kill $SCRAPING_PID $MAIN_PID 2>/dev/null
    pkill -f uvicorn 2>/dev/null
    print_success "Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

print_status "Press Ctrl+C to stop the servers"
echo ""

# Keep script running
while true; do
    sleep 1
done 