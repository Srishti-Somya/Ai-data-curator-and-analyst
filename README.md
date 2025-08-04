# AI Data Curation and Analysis Tool

A comprehensive full-stack application for web scraping, NLP processing, and data visualization with a modern Next.js frontend and FastAPI backend.

## 🏗️ Project Structure

```
Ai_tool_for_dataCuration_analysis/
├── backend/                          # Backend services
│   ├── api/                          # Main API server
│   │   └── master_server.py         # FastAPI main server
│   ├── scraping_service/             # Web scraping service
│   │   ├── main.py                  # Scraping API
│   │   ├── query.py                 # Search functionality
│   │   └── scrapper.py              # Web scraping logic
│   ├── nlp_processing/              # NLP processing
│   │   ├── main.py                  # NLP processing logic
│   │   ├── text_processing.py       # Entity extraction
│   │   ├── visualization.py         # SVG generation
│   │   └── file_utils.py            # File operations
│   ├── data/                        # Generated data files
│   │   ├── scraped_data/            # Scraped content
│   │   ├── structured_data.csv      # Processed CSV
│   │   └── relationships.svg        # Visualizations
│   ├── venv/                        # Python virtual environment
│   └── requirements.txt             # Python dependencies
├── frontend/                        # Next.js frontend
│   ├── src/                         # Source code
│   │   └── app/                     # Next.js app directory
│   ├── package.json                 # Node.js dependencies
│   ├── next.config.js               # Next.js configuration
│   ├── tailwind.config.js           # Tailwind CSS config
│   └── tsconfig.json                # TypeScript config
├── start_full_stack.sh              # Quick start script
├── start_backend.sh                 # Backend start script
├── start_frontend.sh                # Frontend start script
└── README.md                        # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (recommended: 3.10.15)
- **Node.js 16+**
- **Google Chrome** (for web scraping)
- **Git** (for cloning)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Ai_tool_for_dataCuration_analysis
```

### Step 2: Backend Setup

#### Option A: Using the Quick Start Script (Recommended)
```bash
# Make scripts executable
chmod +x start_full_stack.sh start_backend.sh start_frontend.sh

# Run the full stack application
./start_full_stack.sh
```

#### Option B: Manual Setup

1. **Set up Python environment** (if using pyenv):
```bash
cd backend
pyenv local 3.10.15  # or your preferred Python version
```

2. **Activate virtual environment and install dependencies**:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

3. **Install spaCy language model**:
```bash
python -m spacy download en_core_web_lg
```

4. **Start backend services**:
```bash
# Terminal 1: Scraping service
cd backend/scraping_service
uvicorn main:app --port 8001 --reload --host 0.0.0.0 > ../../scraping.log 2>&1 &

# Terminal 2: Main API service
cd backend/api
uvicorn master_server:app --reload --host 0.0.0.0 > ../../main.log 2>&1 &
```

### Step 3: Frontend Setup

#### Option A: Using the Quick Start Script
The frontend will be automatically started by `start_full_stack.sh`.

#### Option B: Manual Setup
```bash
cd frontend
npm install
npm run dev
```

### Step 4: Verify Installation

Check that all services are running:
```bash
# Check frontend
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# Check main API
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/docs

# Check scraping API
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001/docs
```

All should return `200`.

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Main API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Scraping API**: http://127.0.0.1:8001
- **CSV Download**: http://127.0.0.1:8000/csv
- **SVG Download**: http://127.0.0.1:8000/svg

## 🧪 Testing the Application

1. **Open your browser** and go to: http://localhost:3000

2. **Test with example queries**:
   - Query: "python programming"
   - Keywords: ["tutorial", "learning"]
   - Entity Types: ["Person", "Org", "Date", "Loc"]

3. **Expected results**:
   - 15+ pages scraped
   - 20,000+ entities extracted
   - CSV and SVG files generated

## 🔧 Troubleshooting

### Common Issues

#### 1. ChromeDriver Compatibility Error
**Error**: `This version of ChromeDriver only supports Chrome version X`
**Solution**: The application automatically falls back to requests-based scraping when ChromeDriver fails.

#### 2. Python Version Issues
**Error**: `No version is set for command python`
**Solution**: 
```bash
cd backend
pyenv local 3.10.15
python --version  # Should show Python 3.10.15
```

#### 3. Port Already in Use
**Error**: `[Errno 48] Address already in use`
**Solution**: 
```bash
# Stop existing services
pkill -f uvicorn
pkill -f 'next dev'
# Wait 5 seconds, then restart
```

#### 4. Memory Issues with Large Texts
**Error**: `Text of length X exceeds maximum of 1000000`
**Solution**: The application automatically chunks large texts into smaller pieces for processing.

#### 5. Missing Dependencies
**Error**: `ModuleNotFoundError`
**Solution**: 
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Log Files

- **Frontend logs**: `frontend.log`
- **Main API logs**: `main.log`
- **Scraping logs**: `scraping.log`

### Service Management

**Start all services**:
```bash
./start_full_stack.sh
```

**Stop all services**:
```bash
pkill -f uvicorn && pkill -f 'next dev'
```

**Check service status**:
```bash
ps aux | grep uvicorn
ps aux | grep "next dev"
```

## 🎯 Features

- **Web Scraping**: Multi-engine search with Selenium fallback to requests
- **NLP Processing**: Entity extraction with spaCy (supports large texts)
- **Data Visualization**: SVG generation for relationships
- **Modern UI**: Next.js with TypeScript and Tailwind CSS
- **Download Support**: CSV and SVG file downloads
- **Error Handling**: Robust error handling and fallback mechanisms

## 📊 Entity Types Supported

- **Core**: Person, Org, Date, Loc
- **Extended**: Misc, Money, Percent, Time
- **Advanced**: Quantity, Ordinal, Cardinal, Product
- **Additional**: Email, URL, Version, Year

## 🔧 Technologies

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Uvicorn, spaCy 3.7.2, Selenium 4.34.2
- **Data Processing**: Pandas, BeautifulSoup
- **Visualization**: Custom SVG generation
- **Web Scraping**: Selenium with requests fallback

## 📝 Development Notes

- The application handles ChromeDriver compatibility issues automatically
- Large texts are automatically chunked for NLP processing
- Fallback mechanisms ensure robust operation
- All services include comprehensive error handling and logging

## 🛑 Stopping the Application

```bash
# Stop all services
pkill -f uvicorn && pkill -f 'next dev'

# Or use the provided script
./stop_services.sh  # if available
```

The application is now ready for production use! 🚀
