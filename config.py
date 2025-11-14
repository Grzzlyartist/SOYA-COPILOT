"""Configuration management for Soya Copilot."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration from environment variables."""
    
    # AI Model Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Weather API
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    
    # WhatsApp/Twilio Integration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # Data Storage Paths
    CHROMADB_PATH = os.getenv("CHROMADB_PATH", "./data/chromadb")
    MODEL_PATH = os.getenv("MODEL_PATH", "./data/models/yolov8_soybean.pt")
    
    # Application Settings
    MAX_MEMORY = int(os.getenv("MAX_MEMORY", "4"))
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    WHATSAPP_BOT_PORT = int(os.getenv("WHATSAPP_BOT_PORT", "5000"))
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        errors = []
        
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY is not set (required for chat functionality)")
        
        if not cls.OPENWEATHER_API_KEY:
            errors.append("OPENWEATHER_API_KEY is not set (required for location analysis)")
        
        if errors:
            print("⚠️  Configuration warnings:")
            for error in errors:
                print(f"   - {error}")
            print("\nPlease check your .env file and add the required API keys.")
        
        return len(errors) == 0


# Validate configuration on import
Config.validate()
