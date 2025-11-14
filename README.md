# 🌱 Soya Copilot

An AI-powered agricultural assistant for soybean farmers worldwide, with special focus on Southern African farming communities. Features multi-agent capabilities for chat, geo-analysis, and disease detection.

## 🎯 Features

### Multi-Agent System
- **Chat Agent**: Conversational AI with RAG (Retrieval-Augmented Generation) for soybean farming advice
- **Geo Analysis Agent**: Location-based climate suitability analysis using real-time weather data  
- **Disease Detection Agent**: Enhanced image analysis for soybean disease identification
- **Translation Agent**: Multi-language support (coming soon)

### Multiple Interfaces
- **REST API** (FastAPI): Backend service for all agent operations
- **Streamlit Web UI**: Modern chat interface with dark mode, location analysis, and disease detection
- **WhatsApp Bot**: Twilio-powered messaging interface for mobile access

### Language Support
- **Active**: English
- **Coming Soon**: Chichewa, Shona, Zulu, Xhosa, Afrikaans, Swati

### Technologies
- **LLM**: Groq (Llama 3.1 8B Instant)
- **Knowledge Base**: RAG with keyword search fallback (ChromaDB ready)
- **Computer Vision**: Enhanced disease detection with mock analysis
- **Geolocation**: OpenWeather API + Geopy for global weather data

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip or uv package manager

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd soya-copilot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   copy .env.example .env  # Windows
   # cp .env.example .env  # Linux/Mac
   ```
   
   Edit `.env` and add your API keys:
   - `GROQ_API_KEY`: Get from [Groq Console](https://console.groq.com)
   - `OPENWEATHER_API_KEY`: Get from [OpenWeather](https://openweathermap.org/api)
   - `TWILIO_ACCOUNT_SID` & `TWILIO_AUTH_TOKEN`: Get from [Twilio Console](https://console.twilio.com)

### Running the Application

#### Option 1: Quick Start (Recommended)
```bash
# Windows - Double-click the batch file
start_soya_copilot.bat

# Or run manually:
python main.py  # Backend on port 8000
streamlit run frontend/streamlit/app.py  # Frontend on port 8501
```

#### Option 2: Individual Services

**1. FastAPI Backend (Port 8000)**
```bash
python main.py
```
API available at `http://localhost:8000`

**2. Streamlit Web UI (Port 8501)**
```bash
streamlit run frontend/streamlit/app.py
# Or use: start_frontend_only.bat
```
Web interface at `http://localhost:8501`

**3. WhatsApp Bot (Port 5000)**
```bash
python frontend/whatsapp/whatsapp_bot.py
```
Configure Twilio webhook to point to `http://your-server:5000/whatsapp`

## 📁 Project Structure

```
soya-copilot/
├── agents/                          # AI Agent modules
│   ├── chat/                       # Chat agent with RAG
│   │   ├── chat_agent.py          # Main chat orchestrator
│   │   ├── memory_manager.py      # Conversation memory
│   │   └── rag_retriever.py       # Vector DB retrieval
│   ├── geo_analysis/              # Geographic analysis
│   │   └── location_analyzer.py   # Climate suitability checker
│   ├── disease_detection/         # Disease detection
│   │   ├── disease_detector.py    # YOLOv8 disease detector
│   │   └── model_loader.py        # Model management
│   └── orchestrator.py            # Main workflow orchestrator
├── frontend/                       # User interfaces
│   ├── streamlit/                 # Web UI
│   │   └── app.py                 # Streamlit application
│   └── whatsapp/                  # WhatsApp integration
│       └── whatsapp_bot.py        # Twilio webhook handler
├── data/                          # Data storage
│   ├── chromadb/                  # Vector database
│   └── models/                    # ML models (YOLOv8)
├── config.py                      # Configuration management
├── main.py                        # FastAPI backend
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── start_soya_copilot.bat         # Quick start script (Windows)
├── start_frontend_only.bat        # Frontend-only start script
└── README.md                      # This file
```

## 🔌 API Endpoints

### FastAPI Backend (`http://localhost:8000`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status and welcome message |
| GET | `/health` | Health check endpoint |
| POST | `/chat` | Main processing endpoint (accepts text, images, coordinates) |

#### `/chat` Request Format
```bash
curl -X POST "http://localhost:8000/chat" \
  -F "message=What is the best time to plant soybeans?" \
  -F "latitude=-13.9626" \
  -F "longitude=33.7741" \
  -F "image=@soybean_leaf.jpg"
```

#### Response Format
```json
{
  "success": true,
  "response": "The best time to plant soybeans in your region is...",
  "message": "Request processed successfully"
}
```

## 📚 Knowledge Base System

### Current Knowledge Base
The system comes pre-loaded with **162+ agricultural documents** including:
- Soybean production guides
- Disease identification manuals
- Climate and soil management resources
- Regional farming best practices

### How It Works
**Intelligent Retrieval System**:
1. **Primary**: Keyword-based search (fast and reliable)
2. **Fallback**: ChromaDB vector search (when available)
3. **Smart Matching**: Finds relevant information from knowledge base
4. **Contextual Responses**: Generates answers based on retrieved content

### Adding Custom Knowledge
1. **Copy your PDF files** to `data/knowledge/` folder
2. **Restart the application**
3. **Done!** The AI will include your content in responses

**Supported Formats**: PDF (`.pdf`), Text (`.txt`), Markdown (`.md`)

### Testing the System
```bash
python test_knowledge_system.py  # Test knowledge retrieval
python test_disease_detection.py  # Test disease detection
python main.py  # Start the full system
```

## 🌾 Usage Examples

### Chat Agent
Ask farming questions - answers come from comprehensive knowledge base:
- "When should I plant soybeans?"
- "What fertilizer is best for soybeans?"
- "How do I manage soybean rust?"
- "What's the ideal soil pH for soybeans?"

**Features:**
- Conversational memory (remembers context)
- Knowledge-based responses from 162+ agricultural documents
- Keyword search with intelligent fallback

### Location Analysis
Provide coordinates to check climate suitability:
- Real-time weather data analysis
- Temperature and humidity assessment
- Location-specific growing recommendations
- Global coverage via OpenWeather API

### Disease Detection
Upload images of soybean leaves for analysis:
- **Detects**: Bacterial blight, Powdery mildew, Soybean rust, Charcoal rot, Healthy plants
- **Provides**: Confidence scores, Treatment advice, Prevention strategies
- **Note**: Currently uses enhanced mock analysis (TensorFlow model ready)

### Translation Support
Multi-language interface with Southern African focus:
- **Active**: English
- **Coming Soon**: Chichewa, Shona, Zulu, Xhosa, Afrikaans, Swati

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM | Yes |
| `OPENWEATHER_API_KEY` | OpenWeather API key | Yes (for location analysis) |
| `TWILIO_ACCOUNT_SID` | Twilio account SID | Yes (for WhatsApp) |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | Yes (for WhatsApp) |
| `CHROMADB_PATH` | Path to ChromaDB storage | No (default: ./data/chromadb) |
| `MODEL_PATH` | Path to YOLOv8 model | No (default: ./data/models/yolov8_soybean.pt) |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - See LICENSE file for details

## 🚀 Recent Updates

### v1.0.0 - Current Release
- ✅ **Global Scope**: Supports farmers worldwide (no longer Malawi-specific)
- ✅ **Southern African Languages**: Chichewa, Shona, Zulu, Xhosa, Afrikaans, Swati (coming soon)
- ✅ **Enhanced Disease Detection**: Improved mock analysis with realistic predictions
- ✅ **Robust Knowledge System**: 162+ documents with keyword search fallback
- ✅ **Modern UI**: Dark mode, conversation history, improved chat interface
- ✅ **Stable Architecture**: ChromaDB fallback ensures system reliability
- ✅ **Quick Start Scripts**: Easy deployment with batch files
- ✅ **WhatsApp Integration**: Full mobile support via Twilio

## 🛠️ System Status

| Component | Status | Notes |
|-----------|--------|-------|
| Chat Agent | ✅ Active | Groq LLM with conversation memory |
| Knowledge Base | ✅ Active | 162+ documents, keyword search |
| Disease Detection | ✅ Active | Enhanced mock analysis |
| Location Analysis | ✅ Active | Global weather data |
| WhatsApp Bot | ✅ Active | Twilio integration |
| Translation | 🟡 Coming Soon | Southern African languages |
| ChromaDB Vector Search | 🟡 Optional | Keyword fallback available |

## 🙏 Acknowledgments

- Built for soybean farmers worldwide with Southern African focus
- Powered by Groq, LangChain, and enhanced disease detection
- Weather data from OpenWeather API (global coverage)
- WhatsApp integration via Twilio
- Knowledge base includes comprehensive agricultural resources

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting guides in the documentation
- Test individual components using provided test scripts
