"""WhatsApp bot integration using Twilio."""
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import requests
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import Config

app = Flask(__name__)

# Soya Copilot API endpoint
SOYA_API_URL = f"http://localhost:{Config.API_PORT}/chat"

WELCOME_MESSAGE = """🌱 Welcome to Soya Copilot!

I can help you with:
• Soybean farming advice
• Disease detection from images
• Climate suitability analysis
• Multi-language support (coming soon)

Send me a message or image to get started!"""


@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages via Twilio webhook."""
    try:
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        media_url = request.values.get('MediaUrl0')
        
        print(f"📱 Received message from {sender}: {incoming_msg}")
        
        # Handle empty messages
        if not incoming_msg and not media_url:
            response = MessagingResponse()
            response.message(WELCOME_MESSAGE)
            return str(response)
        
        # Prepare payload for Soya Copilot
        payload = {
            "message": incoming_msg or "Analyze this image",
            "latitude": 0.0,
            "longitude": 0.0
        }
        
        # Download and attach image if available
        files = None
        if media_url:
            try:
                print(f"📷 Downloading image from: {media_url}")
                # Download image from Twilio
                img_response = requests.get(media_url, timeout=10)
                if img_response.status_code == 200:
                    files = {"image": ("image.jpg", img_response.content, "image/jpeg")}
                    print("✅ Image downloaded successfully")
            except Exception as e:
                print(f"❌ Error downloading image: {str(e)}")
        
        # Call Soya Copilot API
        try:
            api_response = requests.post(
                SOYA_API_URL,
                data=payload,
                files=files,
                timeout=30
            )
            
            if api_response.status_code == 200:
                result = api_response.json()
                bot_response = result.get('response', 'I apologize, but I encountered an error.')
                print(f"✅ Response generated: {bot_response[:100]}...")
            else:
                print(f"❌ API error: {api_response.status_code}")
                bot_response = WELCOME_MESSAGE
        
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Soya Copilot API")
            bot_response = "Sorry, I'm having trouble connecting to my brain. Please make sure the API is running on port 8000."
        except requests.exceptions.Timeout:
            print("❌ API request timed out")
            bot_response = "Sorry, that's taking too long. Please try again with a simpler question or smaller image."
        
        # Create Twilio response
        twilio_response = MessagingResponse()
        twilio_response.message(bot_response)
        
        return str(twilio_response)
    
    except Exception as e:
        print(f"❌ Error processing WhatsApp message: {str(e)}")
        response = MessagingResponse()
        response.message("Sorry, I'm experiencing technical difficulties. Please try again later.")
        return str(response)


@app.route("/health", methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "whatsapp-bot",
        "api_url": SOYA_API_URL
    })


@app.route("/", methods=['GET'])
def root():
    """Root endpoint."""
    return jsonify({
        "service": "Soya Copilot WhatsApp Bot",
        "status": "running",
        "webhook": "/whatsapp",
        "health": "/health"
    })


if __name__ == "__main__":
    print("🌱 Starting Soya Copilot WhatsApp Bot...")
    print(f"📍 Webhook URL: http://0.0.0.0:{Config.WHATSAPP_BOT_PORT}/whatsapp")
    print(f"🔗 Connecting to API: {SOYA_API_URL}")
    
    if not Config.TWILIO_ACCOUNT_SID or not Config.TWILIO_AUTH_TOKEN:
        print("⚠️  Warning: Twilio credentials not configured in .env")
    
    app.run(
        host="0.0.0.0",
        port=Config.WHATSAPP_BOT_PORT,
        debug=True
    )
