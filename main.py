"""FastAPI backend for Soya Copilot."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from agents.orchestrator import SoyaCopilotOrchestrator
from config import Config
import uvicorn
import logging
import time
import os

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global orchestrator variable
orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifespan events."""
    # Startup
    logger.info("🌱 Soya Copilot API starting...")
    logger.info(f"📍 API running on http://{Config.API_HOST}:{Config.API_PORT}")
    
    # Initialize orchestrator
    global orchestrator
    try:
        orchestrator = SoyaCopilotOrchestrator()
        logger.info("✅ Orchestrator initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize orchestrator: {str(e)}")
        orchestrator = None
    
    # Configuration warnings
    if not Config.GROQ_API_KEY:
        logger.warning("⚠️  GROQ_API_KEY not configured - chat features will not work")
    if not Config.OPENWEATHER_API_KEY:
        logger.warning("⚠️  OPENWEATHER_API_KEY not configured - location analysis will not work")
    
    yield
    
    # Shutdown
    logger.info("🛑 Soya Copilot API shutting down...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Soya Copilot API",
    version="1.0.0",
    description="AI-powered agricultural assistant for soybean farmers worldwide",
    lifespan=lifespan
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"] if os.getenv("ENVIRONMENT") != "production" else ["localhost", "127.0.0.1"]
)

# CORS middleware
allowed_origins = ["*"] if os.getenv("ENVIRONMENT") != "production" else [
    "http://localhost:8501",
    "https://your-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Soya Copilot API is running",
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        }
    }


@app.post("/chat")
async def chat_endpoint(
    message: str = Form(...),
    latitude: float = Form(0.0),
    longitude: float = Form(0.0),
    image: UploadFile = File(None)
):
    """
    Main chat endpoint for processing user requests.
    
    Accepts:
    - message: User's text message
    - latitude: Optional location latitude
    - longitude: Optional location longitude
    - image: Optional image file for disease detection
    """
    if orchestrator is None:
        raise HTTPException(
            status_code=503,
            detail="Service unavailable - orchestrator not initialized"
        )
    
    try:
        # Process image if provided
        image_data = None
        if image:
            logger.info(f"Processing image: {image.filename}")
            image_data = await image.read()
        
        # Log request
        logger.info(f"Processing message: {message[:50]}...")
        
        # Process request through orchestrator
        response = orchestrator.process_request(
            user_message=message,
            image_data=image_data,
            latitude=latitude,
            longitude=longitude
        )
        
        return {
            "success": True,
            "response": response,
            "message": "Request processed successfully"
        }
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            "success": False,
            "response": f"I apologize, but I encountered an error: {str(e)}",
            "message": "Failed to process request"
        }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "soya-copilot",
        "version": "1.0.0",
        "timestamp": time.time(),
        "orchestrator_ready": orchestrator is not None,
        "config": {
            "groq_configured": bool(Config.GROQ_API_KEY),
            "weather_configured": bool(Config.OPENWEATHER_API_KEY),
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    }

@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint."""
    return {
        "service": "soya-copilot",
        "status": "running",
        "orchestrator_status": "ready" if orchestrator else "not_ready"
    }


if __name__ == "__main__":
    logger.info("🚀 Starting Soya Copilot API...")
    uvicorn.run(
        app,
        host=Config.API_HOST,
        port=Config.API_PORT,
        log_level="info"
    )
