"""Orchestrator for routing requests to appropriate agents."""
from agents.chat.chat_agent import ChatAgent
from agents.geo_analysis.location_analyzer import GeoAnalyzer

# Try to import disease detector, but make it optional
try:
    from agents.disease_detection.disease_detector import DiseaseDetector
    DISEASE_DETECTION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Disease detection not available: {e}")
    DISEASE_DETECTION_AVAILABLE = False
    DiseaseDetector = None


class SoyaCopilotOrchestrator:
    """Main orchestrator that routes requests to appropriate agents."""
    
    def __init__(self):
        """Initialize all agents."""
        print("🔧 Initializing agents...")
        self.chat_agent = ChatAgent()
        print("   ✅ Chat agent ready")
        self.geo_analyzer = GeoAnalyzer()
        print("   ✅ Geo analysis agent ready")
        
        if DISEASE_DETECTION_AVAILABLE:
            try:
                self.disease_detector = DiseaseDetector()
                print("   ✅ Disease detection agent ready")
            except Exception as e:
                print(f"   ⚠️  Disease detection failed to initialize: {e}")
                self.disease_detector = None
        else:
            self.disease_detector = None
            print("   ⚠️  Disease detection agent not available (PyTorch/YOLOv8 not installed)")

    def _route_based_on_intent(self, user_message, has_image):
        """
        Determine which agent should handle the request using ReACT reasoning.
        
        THOUGHT: Analyze the user's message and available context to determine intent.
        ACTION: Check for specific keywords and patterns that indicate different agent needs.
        OBSERVATION: Consider both explicit requests and implicit needs based on content.
        """
        message_lower = user_message.lower()
        
        # THOUGHT: What is the user asking for?
        
        # ACTION: Check for translation intent first
        translation_keywords = ['translate', 'translation', 'chichewa', 'shona', 'zulu', 'xhosa', 'afrikaans', 'swati', 'language']
        if any(word in message_lower for word in translation_keywords):
            # OBSERVATION: User explicitly wants translation services
            return "translation"
        
        # ACTION: Check for location/weather analysis intent
        location_keywords = ['location', 'weather', 'climate', 'suitable', 'temperature', 'rainfall', 'humidity', 'region', 'area']
        if any(word in message_lower for word in location_keywords):
            # OBSERVATION: User wants location-specific farming advice
            return "location_analysis"
        
        # ACTION: Check for disease detection intent
        disease_keywords = ['disease', 'sick', 'problem', 'spots', 'leaves', 'infection', 'pest', 'damage', 'dying']
        if has_image or any(word in message_lower for word in disease_keywords):
            # OBSERVATION: User has plant health concerns or uploaded an image
            return "disease_detection"
        
        # ACTION: Default to general chat for farming advice
        # OBSERVATION: General farming questions, advice, or conversation
        return "chat"

    def _process_chat(self, user_message):
        """Process general chat requests."""
        return self.chat_agent.process_message(user_message)

    def _process_translation(self, user_message):
        """Process translation requests."""
        return ("🚧 **Translation Feature Coming Soon!**\n\n"
                "We're working on adding multi-language translation capabilities to help farmers worldwide.\n\n"
                "**What's coming:**\n"
                "• Real-time text translation\n"
                "• Voice message translation\n"
                "• Agricultural terminology support\n"
                "• Multiple language support\n"
                "• Offline translation capabilities\n\n"
                "For now, I can help you in English with all your soybean farming questions!\n\n"
                "**Ask me about:**\n"
                "• Planting and cultivation\n"
                "• Disease identification\n"
                "• Climate and weather guidance\n"
                "• Soil management\n"
                "• Harvest timing")



    def _process_location(self, latitude, longitude):
        """Process location analysis requests."""
        if latitude == 0 and longitude == 0:
            return "Please provide your location coordinates for climate analysis."
        
        analysis = self.geo_analyzer.analyze_soybean_suitability(latitude, longitude)
        
        # Format response
        if analysis.get('suitable'):
            response = f"✅ Location suitable for soybeans!\n"
        else:
            response = f"⚠️ Location may need adjustments for soybeans.\n"
        
        if 'temperature' in analysis:
            response += f"Temperature: {analysis['temperature']:.1f}°C\n"
        if 'humidity' in analysis:
            response += f"Humidity: {analysis['humidity']}%\n"
        
        if 'recommendations' in analysis:
            response += "\nRecommendations:\n"
            response += "\n".join(f"• {rec}" for rec in analysis['recommendations'])
        
        return response

    def _process_disease(self, image_data):
        """Process disease detection requests."""
        if not self.disease_detector:
            return ("⚠️ **Disease Detection Unavailable**\n\n"
                   "Disease detection requires a trained TensorFlow model and proper setup.\n\n"
                   "**To enable disease detection:**\n"
                   "1. Install TensorFlow: `pip install tensorflow`\n"
                   "2. Place a trained model at: `./data/models/soybean_diseased_leaf_inceptionv3_model.keras`\n"
                   "3. Restart the application\n\n"
                   "**For now:**\n"
                   "• Consult a local agricultural expert\n"
                   "• Contact your extension officer\n"
                   "• Use visual disease identification guides\n"
                   "• Take clear photos and seek professional advice")
        
        if not image_data:
            return ("📷 **Image Required for Disease Detection**\n\n"
                   "Please upload a clear image of soybean leaves showing:\n"
                   "• Close-up view of affected areas\n"
                   "• Good lighting conditions\n"
                   "• Multiple leaves if possible\n"
                   "• Focus on symptoms (spots, discoloration, etc.)")
        
        try:
            detections = self.disease_detector.detect_disease(image_data)
            
            if not detections:
                return "❌ No analysis results available. Please try with a different image."
            
            detection = detections[0]  # Get first detection
            disease_name = detection['disease'].replace('_', ' ').title()
            
            # Handle special cases
            if detection['disease'] == 'unavailable':
                return ("⚠️ **Disease Detection Currently Unavailable**\n\n"
                       f"**Issue:** {detection['treatment']}\n\n"
                       f"**Recommendation:** {detection['prevention']}\n\n"
                       f"**Note:** {detection.get('note', '')}")
            
            if detection['disease'] == 'error':
                return ("❌ **Image Analysis Failed**\n\n"
                       f"**Error:** {detection['treatment']}\n\n"
                       f"**Suggestion:** {detection['prevention']}\n\n"
                       f"**Note:** {detection.get('note', '')}")
            
            # Normal detection result
            is_demo = detection.get('is_demo', False)
            
            if is_demo:
                response = "🎭 **Disease Analysis - DEMONSTRATION MODE**\n\n"
            else:
                response = "🌱 **Disease Analysis Results**\n\n"
            
            response += f"🔍 **Detection:** {disease_name}\n"
            
            if detection['confidence'] > 0:
                response += f"📊 **Confidence:** {detection['confidence']:.1%}\n"
            
            response += f"💊 **Treatment:** {detection['treatment']}\n"
            response += f"🛡️ **Prevention:** {detection['prevention']}\n"
            
            # Add detailed predictions if available
            if detection.get('all_predictions') and len(detection['all_predictions']) > 1:
                response += "\n📈 **Detailed Analysis:**\n"
                sorted_predictions = sorted(
                    detection['all_predictions'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
                for disease, prob in sorted_predictions[:3]:  # Top 3
                    disease_display = disease.replace('_', ' ').title()
                    response += f"   • {disease_display}: {prob:.1%}\n"
            
            if detection.get('note'):
                response += f"\n📝 **Important:** {detection['note']}\n"
            
            if not is_demo:
                response += "\n⚠️ **Recommendation:** Always consult an agricultural expert for confirmation and professional advice."
            
            return response
            
        except Exception as e:
            return (f"❌ **Analysis Error**\n\n"
                   f"**Error:** {str(e)}\n\n"
                   "**Suggestions:**\n"
                   "• Try with a different image\n"
                   "• Ensure image is clear and well-lit\n"
                   "• Check image format (JPG, PNG)\n"
                   "• Consult an agricultural expert\n\n"
                   "**Note:** If this problem persists, the disease detection model may not be properly configured.")

    def process_request(self, user_message, image_data=None, latitude=0, longitude=0):
        """
        Main entry point for processing requests.
        
        Args:
            user_message: User's text message
            image_data: Optional image bytes for disease detection
            latitude: Optional latitude for location analysis
            longitude: Optional longitude for location analysis
            
        Returns:
            str: Response from the appropriate agent
        """
        try:
            # Determine intent
            intent = self._route_based_on_intent(user_message, image_data is not None)
            
            # Route to appropriate agent
            if intent == "translation":
                response = self._process_translation(user_message)
            
            elif intent == "location_analysis":
                response = self._process_location(latitude, longitude)
            
            elif intent == "disease_detection":
                response = self._process_disease(image_data)
            
            else:  # chat
                response = self._process_chat(user_message)
            
            return response
        
        except Exception as e:
            error_msg = f"I apologize, but I encountered an error: {str(e)}\nPlease try again or rephrase your question."
            return error_msg
