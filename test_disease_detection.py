#!/usr/bin/env python3
"""
Test script for disease detection using the InceptionV3 model.
"""

import os
import sys
from PIL import Image
from agents.disease_detection.disease_detector import DiseaseDetector


def test_disease_detection():
    """Test the disease detection functionality."""
    
    # Initialize the disease detector
    print("Initializing disease detector...")
    detector = DiseaseDetector()
    
    # Check if model exists
    model_path = "./data/models/soybean_diseased_leaf_inceptionv3_model.keras"
    if not os.path.exists(model_path):
        print(f"❌ Model not found at {model_path}")
        print("Please ensure the model file exists in the data/models directory.")
        return False
    
    print(f"✅ Model found at {model_path}")
    
    # Check for test images
    image_dir = "./data/images"
    if not os.path.exists(image_dir):
        print(f"📁 Creating images directory at {image_dir}")
        os.makedirs(image_dir, exist_ok=True)
    
    # Look for any image files in the images directory
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = []
    
    if os.path.exists(image_dir):
        for file in os.listdir(image_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(image_dir, file))
    
    if not image_files:
        print(f"📷 No test images found in {image_dir}")
        print("Please add some soybean leaf images to test the detection.")
        print("Supported formats: JPG, PNG, BMP, TIFF")
        return False
    
    print(f"📷 Found {len(image_files)} test image(s)")
    
    # Test detection on each image
    for image_path in image_files:
        print(f"\n🔍 Testing detection on: {os.path.basename(image_path)}")
        
        try:
            # Load and process image
            image = Image.open(image_path)
            print(f"   Image size: {image.size}")
            
            # Perform disease detection
            results = detector.detect_disease(image)
            
            # Display results
            for i, result in enumerate(results):
                print(f"   Result {i+1}:")
                print(f"     Disease: {result['disease']}")
                print(f"     Confidence: {result['confidence']:.3f}")
                print(f"     Treatment: {result['treatment']}")
                print(f"     Prevention: {result['prevention']}")
                
                if 'all_predictions' in result and result['all_predictions']:
                    print(f"     All predictions:")
                    for disease, prob in result['all_predictions'].items():
                        print(f"       {disease}: {prob:.3f}")
        
        except Exception as e:
            print(f"   ❌ Error processing {image_path}: {str(e)}")
    
    return True


def create_sample_test():
    """Create a sample test with a simple colored image if no real images are available."""
    
    print("\n🎨 Creating a sample test image...")
    
    # Create a simple test image
    from PIL import Image, ImageDraw
    import numpy as np
    
    # Create a 299x299 RGB image (InceptionV3 input size)
    img = Image.new('RGB', (299, 299), color='green')
    draw = ImageDraw.Draw(img)
    
    # Add some simple patterns to simulate a leaf
    draw.ellipse([50, 50, 249, 249], fill='lightgreen', outline='darkgreen')
    draw.ellipse([100, 100, 199, 199], fill='yellow', outline='brown')  # Simulate disease spot
    
    # Save the test image
    os.makedirs('./data/images', exist_ok=True)
    test_image_path = './data/images/sample_leaf.png'
    img.save(test_image_path)
    
    print(f"✅ Sample test image created: {test_image_path}")
    
    # Test with the sample image
    detector = DiseaseDetector()
    results = detector.detect_disease(img)
    
    print(f"\n🔍 Sample detection results:")
    for result in results:
        print(f"   Disease: {result['disease']}")
        print(f"   Confidence: {result['confidence']:.3f}")
        print(f"   Treatment: {result['treatment']}")


if __name__ == "__main__":
    print("🌱 Soybean Disease Detection Test")
    print("=" * 40)
    
    try:
        success = test_disease_detection()
        
        if not success:
            print("\n🎨 Running with sample image instead...")
            create_sample_test()
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure TensorFlow is installed: pip install tensorflow")
        print("2. Check that the model file exists and is valid")
        print("3. Verify image files are in the correct format")
        
    print("\n✅ Test completed!")