import os
import numpy as np
from PIL import Image

# Try to import TensorFlow
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️  TensorFlow not available, using mock model")

# Mock model for demonstration when real model is not available
class MockDiseaseModel:
    """
    Mock disease detection model for demonstration purposes.
    Provides realistic-looking results based on basic image analysis.
    """
    
    def __init__(self):
        self.loaded = True
        self.is_mock = True
        print("⚠️  Using mock disease detection model for demonstration")
    
    def predict(self, image_array, verbose=0):
        """
        Mock prediction that analyzes basic image characteristics.
        Returns realistic probability distributions for demonstration.
        """
        try:
            # Analyze image characteristics
            if len(image_array.shape) == 4:
                img = image_array[0]  # Remove batch dimension
            else:
                img = image_array
            
            # Basic image analysis for more realistic results
            mean_brightness = np.mean(img)
            
            # Analyze color channels if available
            if len(img.shape) == 3 and img.shape[2] >= 3:
                green_channel = np.mean(img[:, :, 1])
                red_channel = np.mean(img[:, :, 0])
                blue_channel = np.mean(img[:, :, 2])
            else:
                green_channel = red_channel = blue_channel = mean_brightness
            
            # Create realistic probabilities based on image characteristics
            # This is for demonstration - real model would use trained weights
            
            if green_channel > 0.6 and mean_brightness > 0.5:
                # Bright green image - likely healthy
                probabilities = [0.75, 0.08, 0.05, 0.04, 0.04, 0.04]
            elif red_channel > green_channel and red_channel > 0.4:
                # Reddish tones - might indicate rust or blight
                probabilities = [0.15, 0.35, 0.15, 0.25, 0.05, 0.05]
            elif mean_brightness < 0.3:
                # Dark image - might indicate severe disease or rot
                probabilities = [0.05, 0.15, 0.15, 0.15, 0.40, 0.10]
            elif green_channel < 0.4:
                # Low green content - possible disease
                probabilities = [0.20, 0.25, 0.20, 0.15, 0.10, 0.10]
            else:
                # Mixed characteristics - uncertain
                probabilities = [0.30, 0.20, 0.15, 0.15, 0.10, 0.10]
            
            # Add slight randomness for more realistic variation
            np.random.seed(int(mean_brightness * 1000) % 100)  # Deterministic but varied
            noise = np.random.normal(0, 0.03, 6)
            probabilities = np.array(probabilities) + noise
            
            # Ensure probabilities are positive and sum to 1
            probabilities = np.abs(probabilities)
            probabilities = probabilities / np.sum(probabilities)
            
            return np.array([probabilities])
            
        except Exception as e:
            print(f"Error in mock prediction: {e}")
            # Fallback to default probabilities
            return np.array([[0.4, 0.2, 0.15, 0.1, 0.1, 0.05]])


class ModelLoader:
    def __init__(self, model_path="./data/models/soybean_diseased_leaf_inceptionv3_model.keras"):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        # First try to load real TensorFlow model
        if os.path.exists(self.model_path) and TENSORFLOW_AVAILABLE:
            try:
                print(f"📁 Loading TensorFlow model from {self.model_path}")
                self.model = tf.keras.models.load_model(self.model_path)
                print("✅ Real TensorFlow model loaded successfully")
                return self.model
            except Exception as e:
                print(f"❌ Failed to load TensorFlow model: {e}")
                print("   Falling back to mock model for demonstration")
        
        # Fallback to mock model for demonstration
        if not os.path.exists(self.model_path):
            print(f"⚠️  Model not found at {self.model_path}")
        
        if not TENSORFLOW_AVAILABLE:
            print("⚠️  TensorFlow not available")
        
        print("🎭 Loading mock disease detection model for demonstration")
        self.model = MockDiseaseModel()
        return self.model

    def ensure_model_loaded(self):
        if self.model is None:
            self.load_model()

    def preprocess_image(self, image, target_size=(299, 299)):
        """Preprocess image for InceptionV3 model"""
        if hasattr(image, 'resize'):
            # PIL Image
            image = image.resize(target_size)
            image_array = np.array(image)
        else:
            # numpy array
            image_array = image
        
        # Ensure RGB format
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            pass  # Already RGB
        elif len(image_array.shape) == 3 and image_array.shape[2] == 4:
            # RGBA to RGB
            image_array = image_array[:, :, :3]
        
        # Resize if needed using PIL
        if image_array.shape[:2] != target_size:
            pil_image = Image.fromarray(image_array.astype('uint8'))
            pil_image = pil_image.resize(target_size)
            image_array = np.array(pil_image)
        
        # Normalize to [0, 1] range
        image_array = image_array.astype(np.float32) / 255.0
        
        # Add batch dimension
        return np.expand_dims(image_array, axis=0)
