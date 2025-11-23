# 🌱 Soya Copilot

An AI-powered agricultural assistant for soybean farmers worldwide, with special focus on Southern African farming communities. Features multi-agent capabilities with ReACT reasoning, RAG-based knowledge retrieval, geo-analysis, and disease detection.

## 🎯 Features

### Multi-Agent System with ReACT Reasoning
- **Chat Agent**: Conversational AI with RAG (Retrieval-Augmented Generation) and ReACT reasoning for intelligent soybean farming advice
- **ReACT Reasoning Agent**: Structured reasoning framework (THOUGHT → ACTION → OBSERVATION → RESPONSE) for better decision-making
- **Geo Analysis Agent**: Location-based climate suitability analysis using real-time weather data  
- **Disease Detection Agent**: TensorFlow/Keras-based image analysis for soybean disease identification
- **Translation Agent**: Multi-language support (coming soon)

### Multiple Interfaces
- **REST API** (FastAPI): Production-ready backend service for all agent operations with health checks and metrics
- **Streamlit Web UI**: Modern chat interface with dark mode, conversation history, location analysis, and disease detection
- **WhatsApp Bot**: Twilio-powered messaging interface for mobile access

### Language Support
- **Active**: English
- **Coming Soon**: Chichewa, Shona, Zulu, Xhosa, Afrikaans, Swati

### Technologies
- **LLM**: Groq API (Llama 3.1 8B Instant)
- **Knowledge Base**: RAG with ChromaDB vector search and keyword search fallback
- **Computer Vision**: TensorFlow/Keras disease detection models (InceptionV3)
- **Geolocation**: OpenWeather API + Geopy for global weather data
- **Framework**: LangChain for agent orchestration and RAG

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
start_all.bat

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
│   │   ├── chat_agent.py          # Main chat agent with ReACT integration
│   │   ├── memory_manager.py      # Conversation memory management
│   │   └── rag_retriever.py       # Vector DB & keyword retrieval
│   ├── reasoning/                  # Reasoning framework
│   │   └── react_agent.py         # ReACT reasoning implementation
│   ├── geo_analysis/              # Geographic analysis
│   │   └── location_analyzer.py   # Climate suitability checker
│   ├── disease_detection/         # Disease detection
│   │   ├── disease_detector.py    # TensorFlow/Keras disease detector
│   │   └── model_loader.py        # Model loading and preprocessing
│   └── orchestrator.py            # Main workflow orchestrator
├── frontend/                       # User interfaces
│   ├── streamlit/                 # Web UI
│   │   └── app.py                 # Streamlit application with dark mode
│   └── whatsapp/                  # WhatsApp integration
│       └── whatsapp_bot.py        # Twilio webhook handler
├── data/                          # Data storage
│   ├── chromadb/                  # Vector database storage
│   ├── models/                    # ML models (TensorFlow/Keras)
│   └── knowledge/                 # Knowledge base documents
│       ├── diseases/              # Disease-related PDFs
│       └── soybean_farming/       # Farming guides and resources
├── logs/                          # Application logs
├── config.py                      # Configuration management
├── main.py                        # FastAPI backend with lifespan events
├── requirements.txt               # Python dependencies
├── requirements-production.txt    # Production dependencies
├── requirements-minimal.txt       # Minimal dependencies
├── .env.example                   # Environment variables template
├── production.env.example         # Production environment template
├── start_all.bat                  # Quick start script (Windows)
├── setup.bat                      # Setup script (Windows)
├── deploy.bat / deploy.sh         # Deployment scripts
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker image definition
└── README.md                      # This file
```

## 🔌 API Endpoints

### FastAPI Backend (`http://localhost:8000`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status and welcome message |
| GET | `/health` | Health check endpoint with system status |
| GET | `/metrics` | Basic metrics endpoint |
| GET | `/docs` | Interactive API documentation (Swagger UI) |
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
- Soybean production guides from various regions
- Disease identification and management manuals
- Climate and soil management resources
- Regional farming best practices
- Market and economic analysis reports

### How It Works
**Intelligent Retrieval System with ReACT Reasoning**:
1. **Intent Analysis**: ReACT reasoning determines user intent and required actions
2. **Dual Retrieval Strategy**: 
   - **Primary**: ChromaDB vector search for semantic similarity
   - **Fallback**: Keyword-based search for reliability
3. **Context Assembly**: Retrieves top 5 most relevant document chunks
4. **ReACT Processing**: Applies structured reasoning (THOUGHT → ACTION → OBSERVATION)
5. **Contextual Responses**: Generates answers based on retrieved content and reasoning

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
Ask farming questions - answers come from comprehensive knowledge base with intelligent reasoning:
- "When should I plant soybeans?"
- "What fertilizer is best for soybeans?"
- "How do I manage soybean rust?"
- "What's the ideal soil pH for soybeans?"

**Features:**
- **ReACT Reasoning**: Structured reasoning for better responses
- **Conversational Memory**: Remembers context across multiple interactions (configurable up to 4 messages)
- **Knowledge-Based Responses**: Pulls from 162+ agricultural documents
- **Dual Retrieval**: ChromaDB vector search with keyword search fallback
- **Context-Aware**: Understands question types and farming domains

### Location Analysis
Provide coordinates to check climate suitability:
- Real-time weather data analysis
- Temperature and humidity assessment
- Location-specific growing recommendations
- Global coverage via OpenWeather API

### Disease Detection
Upload images of soybean leaves for AI-powered analysis:
- **Detects**: Healthy, Bacterial blight, Powdery mildew, Soybean rust, Charcoal rot, Frogeye leaf spot
- **Provides**: Confidence scores, detailed predictions, Treatment advice, Prevention strategies
- **Technology**: TensorFlow/Keras models (InceptionV3 architecture)
- **Model Support**: Automatic model loading with graceful fallback if model unavailable

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
| `TWILIO_ACCOUNT_SID` | Twilio account SID | Optional (for WhatsApp) |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | Optional (for WhatsApp) |
| `TWILIO_PHONE_NUMBER` | Twilio WhatsApp number | Optional (for WhatsApp) |
| `CHROMADB_PATH` | Path to ChromaDB storage | No (default: ./data/chromadb) |
| `MODEL_PATH` | Path to TensorFlow/Keras model | No (default: ./data/models/soybean_diseased_leaf_inceptionv3_model.keras) |
| `LLM_MODEL` | LLM model name | No (default: llama-3.1-8b-instant) |
| `MAX_MEMORY` | Conversation memory size | No (default: 4) |
| `API_HOST` | API host address | No (default: 0.0.0.0) |
| `API_PORT` | API port number | No (default: 8000) |
| `LOG_LEVEL` | Logging level | No (default: INFO) |
| `ENVIRONMENT` | Environment (development/production) | No (default: development) |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - See LICENSE file for details

## 🚀 Recent Updates

### v1.0.0 - Current Release
- ✅ **ReACT Reasoning**: Structured reasoning framework for intelligent responses
- ✅ **Global Scope**: Supports farmers worldwide with location-specific advice
- ✅ **Enhanced Disease Detection**: TensorFlow/Keras-based image analysis with confidence scores
- ✅ **Robust Knowledge System**: 162+ documents with dual retrieval (vector + keyword search)
- ✅ **Modern UI**: Dark mode, conversation history, improved chat interface
- ✅ **Production Ready**: Docker support, health checks, metrics endpoint, logging
- ✅ **Stable Architecture**: ChromaDB with keyword fallback ensures system reliability
- ✅ **Quick Start Scripts**: Easy deployment with batch files and Docker
- ✅ **WhatsApp Integration**: Full mobile support via Twilio
- ✅ **Southern African Languages**: Chichewa, Shona, Zulu, Xhosa, Afrikaans, Swati (coming soon)

## 🛠️ System Status

| Component | Status | Notes |
|-----------|--------|-------|
| Chat Agent | ✅ Active | Groq LLM with ReACT reasoning & conversation memory |
| ReACT Reasoning | ✅ Active | Structured reasoning framework for better responses |
| Knowledge Base | ✅ Active | 162+ documents, dual retrieval (vector + keyword) |
| Disease Detection | ✅ Active | TensorFlow/Keras models with confidence scores |
| Location Analysis | ✅ Active | Global weather data via OpenWeather API |
| WhatsApp Bot | ✅ Active | Twilio integration (optional) |
| Translation | 🟡 Coming Soon | Southern African languages |
| ChromaDB Vector Search | ✅ Active | With keyword search fallback |

## 🚀 Deployment

### Docker Deployment (Recommended)
```bash
# Copy production environment file
cp production.env.example .env
# Edit .env with your API keys

# Deploy with Docker Compose
docker-compose up -d

# Check health
python health_check.py
```

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment guide including:
- Docker deployment
- Manual server setup
- Reverse proxy configuration (Nginx)
- Monitoring and logging
- Security considerations
- Scaling strategies

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py

# Run frontend
streamlit run frontend/streamlit/app.py
```

## 🧪 Testing

```bash
# Test knowledge system
python test_knowledge_system.py

# Test disease detection
python test_disease_detection.py
python test_mock_disease_detection.py

# Test API endpoints
python test_api.py

# Test ReACT reasoning
python test_react_reasoning.py

# Health check
python health_check.py
```

## 🙏 Acknowledgments

- Built for soybean farmers worldwide with Southern African focus
- Powered by Groq, LangChain, TensorFlow, and ReACT reasoning framework
- Weather data from OpenWeather API (global coverage)
- WhatsApp integration via Twilio
- Knowledge base includes comprehensive agricultural resources from various institutions

## 📞 Support & Documentation

- **Main Documentation**: This README
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Adding Knowledge**: [HOW_TO_ADD_KNOWLEDGE.md](HOW_TO_ADD_KNOWLEDGE.md)
- **Backend Deployment**: [BACKEND_DEPLOYMENT.md](BACKEND_DEPLOYMENT.md)
- **Production Checklist**: [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)
- **GitHub Setup**: [GITHUB_SETUP.md](GITHUB_SETUP.md)

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting guides in the documentation
- Test individual components using provided test scripts
- Review logs in `logs/app.log`

## APP URL
- https://soya-copilot-lmbv7rafdh8fi48xxgt2fl.streamlit.app/
  
