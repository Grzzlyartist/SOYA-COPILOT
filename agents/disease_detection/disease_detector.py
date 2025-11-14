from .model_loader import ModelLoader
import numpy as np
from PIL import Image
import io


class DiseaseDetector:
    def __init__(self, model_path="./data/models/soybean_diseased_leaf_inceptionv3_model.keras"):
        self.model_loader = ModelLoader(model_path)
        # Common soybean disease classes - adjust based on your model's training
        self.disease_classes = [
            'healthy',
            'bacterial_blight',
            'powdery_mildew', 
            'soybean_rust',
            'charcoal_rot',
            'frogeye_leaf_spot'
        ]
        self.using_mock = not hasattr(self.model_loader, 'model') or isinstance(self.model_loader.model, type(None))

    def detect_disease(self, image_data):
        self.model_loader.ensure_model_loaded()
        
        # Check if model is available
        if not self.model_loader.model:
            return [{
                'disease': 'unavailable',
                'confidence': 0.0,
                'treatment': 'Disease detection is currently unavailable. No model found.',
                'prevention': 'For disease identification, please consult a local agricultural expert or extension officer.',
                'note': 'To enable real disease detection, place a trained model file at: ./data/models/soybean_diseased_leaf_inceptionv3_model.keras',
                'is_demo': False,
                'all_predictions': {}
            }]
        
        try:
            # Convert image data if needed
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data
            
            # Preprocess image
            processed_image = self.model_loader.preprocess_image(image)
            
            # Perform prediction
            predictions = self.model_loader.model.predict(processed_image, verbose=0)
            
            # Get the class with highest probability
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Map to disease class
            if predicted_class_idx < len(self.disease_classes):
                disease = self.disease_classes[predicted_class_idx]
            else:
                disease = 'unknown'
            
            # Check if using mock model
            is_mock = hasattr(self.model_loader.model, 'is_mock') and self.model_loader.model.is_mock
            
            # Create appropriate note based on model type
            if is_mock:
                note = ("🎭 DEMONSTRATION MODE: This analysis is for demonstration purposes only. "
                       "Results are based on basic image analysis, not a trained AI model. "
                       "For accurate disease diagnosis, please consult an agricultural expert.")
            else:
                note = ("🤖 AI-POWERED ANALYSIS: Results from trained disease detection model. "
                       "For confirmation and treatment advice, consult an agricultural expert.")
            
            # Return detection result
            detection = {
                'disease': disease,
                'confidence': confidence,
                'treatment': self.get_treatment_advice(disease),
                'prevention': self.get_prevention_advice(disease),
                'note': note,
                'is_demo': is_mock,
                'all_predictions': {
                    self.disease_classes[i]: float(predictions[0][i]) 
                    for i in range(min(len(self.disease_classes), len(predictions[0])))
                }
            }
            
            return [detection]
        
        except Exception as e:
            return [{
                'disease': 'error',
                'confidence': 0.0,
                'treatment': f'Detection error: {str(e)}',
                'prevention': 'Please try with a clearer image or consult an agricultural expert.',
                'note': 'Image analysis failed. Please ensure the image is clear and shows soybean leaves.',
                'is_demo': False,
                'all_predictions': {}
            }]

    def get_treatment_advice(self, disease):
        treatments = {
            'healthy': "Your soybeans look healthy! Continue good farming practices.",
            'bacterial_blight': "Apply copper-based bactericides. Remove infected plants. Avoid overhead irrigation.",
            'powdery_mildew': "Use sulfur-based fungicides. Improve air circulation. Remove infected leaves.",
            'soybean_rust': "Apply fungicides containing triazoles. Plant resistant varieties. Practice crop rotation.",
            'charcoal_rot': "Improve soil drainage. Use resistant varieties. Avoid water stress.",
            'frogeye_leaf_spot': "Apply fungicides with active ingredients like azoxystrobin. Remove crop debris.",
            'unavailable': "Disease detection is currently unavailable. No trained model found.",
            'error': "Image analysis failed. Please try with a clearer image.",
            'unknown': "Consult local agricultural expert for accurate diagnosis."
        }
        return treatments.get(disease, "Consult agricultural expert for proper diagnosis and treatment.")

    def get_prevention_advice(self, disease):
        prevention = {
            'healthy': "Maintain soil health with organic matter and proper pH levels.",
            'bacterial_blight': "Use disease-free seeds. Practice crop rotation. Avoid working in wet fields.",
            'powdery_mildew': "Ensure proper plant spacing. Monitor humidity levels. Use resistant varieties.",
            'soybean_rust': "Plant early-maturing varieties. Monitor weather conditions. Use certified seeds.",
            'charcoal_rot': "Improve soil organic matter. Avoid drought stress. Practice rotation with non-host crops.",
            'frogeye_leaf_spot': "Use certified disease-free seeds. Practice crop rotation. Manage crop residue.",
            'unavailable': "Regular field monitoring and consulting agricultural experts can help identify diseases early.",
            'error': "Ensure images are clear and well-lit. Focus on affected plant parts.",
            'unknown': "Regular field monitoring and maintaining plant health can prevent many diseases."
        }
        return prevention.get(disease, "Regular monitoring, good agricultural practices, and expert consultation are essential.")
