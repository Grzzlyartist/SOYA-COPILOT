#!/usr/bin/env python3
"""
Disease Detection Demo - Interactive CLI for testing soybean disease detection
"""

import os
import sys
from PIL import Image
from agents.disease_detection.disease_detector import DiseaseDetector


def print_banner():
    """Print a nice banner for the demo"""
    print("=" * 60)
    print("🌱 SOYBEAN DISEASE DETECTION SYSTEM")
    print("=" * 60)
    print("This system analyzes soybean leaf images to detect diseases")
    print("and provides treatment recommendations.")
    print()


def print_detection_results(results, image_name=""):
    """Print detection results in a formatted way"""
    print(f"📊 DETECTION RESULTS {f'for {image_name}' if image_name else ''}")
    print("-" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"Detection #{i}:")
        print(f"  🔍 Disease: {result['disease'].upper()}")
        print(f"  📈 Confidence: {result['confidence']:.1%}")
        print(f"  💊 Treatment: {result['treatment']}")
        print(f"  🛡️  Prevention: {result['prevention']}")
        
        if 'all_predictions' in result and result['all_predictions']:
            print(f"  📋 All Predictions:")
            sorted_predictions = sorted(
                result['all_predictions'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            for disease, prob in sorted_predictions:
                print(f"     {disease}: {prob:.1%}")
        print()


def analyze_image(detector, image_path):
    """Analyze a single image"""
    try:
        print(f"🔍 Analyzing: {os.path.basename(image_path)}")
        
        # Load image
        image = Image.open(image_path)
        print(f"   📐 Image size: {image.size}")
        print(f"   🎨 Image mode: {image.mode}")
        
        # Perform detection
        results = detector.detect_disease(image)
        
        # Display results
        print_detection_results(results, os.path.basename(image_path))
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing {image_path}: {str(e)}")
        return False


def interactive_mode():
    """Run interactive mode for testing"""
    print_banner()
    
    # Initialize detector
    print("🚀 Initializing disease detector...")
    detector = DiseaseDetector()
    print("✅ Disease detector ready!")
    print()
    
    while True:
        print("OPTIONS:")
        print("1. Analyze image file")
        print("2. Analyze all images in data/images folder")
        print("3. Create and analyze sample image")
        print("4. Show disease information")
        print("5. Exit")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            image_path = input("Enter image path: ").strip()
            if os.path.exists(image_path):
                analyze_image(detector, image_path)
            else:
                print(f"❌ File not found: {image_path}")
        
        elif choice == '2':
            image_dir = "./data/images"
            if not os.path.exists(image_dir):
                print(f"❌ Directory not found: {image_dir}")
                continue
                
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
            image_files = [
                os.path.join(image_dir, f) 
                for f in os.listdir(image_dir)
                if any(f.lower().endswith(ext) for ext in image_extensions)
            ]
            
            if not image_files:
                print(f"📷 No images found in {image_dir}")
            else:
                print(f"📷 Found {len(image_files)} image(s)")
                for image_path in image_files:
                    analyze_image(detector, image_path)
        
        elif choice == '3':
            create_sample_and_analyze(detector)
        
        elif choice == '4':
            show_disease_info()
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")
        
        print("\n" + "="*60 + "\n")


def create_sample_and_analyze(detector):
    """Create a sample image and analyze it"""
    from PIL import ImageDraw
    
    print("🎨 Creating sample soybean leaf image...")
    
    # Create a realistic-looking leaf image
    img = Image.new('RGB', (400, 300), color='lightgreen')
    draw = ImageDraw.Draw(img)
    
    # Draw leaf shape
    draw.ellipse([50, 50, 350, 250], fill='green', outline='darkgreen', width=3)
    
    # Add some disease-like spots
    draw.ellipse([150, 100, 180, 130], fill='brown', outline='darkbrown')
    draw.ellipse([200, 150, 220, 170], fill='yellow', outline='orange')
    draw.ellipse([120, 180, 140, 200], fill='gray', outline='black')
    
    # Add leaf veins
    draw.line([200, 50, 200, 250], fill='darkgreen', width=2)
    draw.line([100, 150, 300, 150], fill='darkgreen', width=1)
    
    # Save sample image
    os.makedirs('./data/images', exist_ok=True)
    sample_path = './data/images/sample_diseased_leaf.png'
    img.save(sample_path)
    
    print(f"✅ Sample image created: {sample_path}")
    
    # Analyze the sample
    analyze_image(detector, sample_path)


def show_disease_info():
    """Show information about different diseases"""
    print("🦠 SOYBEAN DISEASE INFORMATION")
    print("-" * 40)
    
    diseases = {
        'healthy': {
            'description': 'No disease detected - healthy soybean leaves',
            'symptoms': 'Green, vibrant leaves with no spots or discoloration',
            'causes': 'Good growing conditions and plant health'
        },
        'bacterial_blight': {
            'description': 'Bacterial infection causing leaf spots and blight',
            'symptoms': 'Brown spots with yellow halos, leaf wilting',
            'causes': 'Wet conditions, poor air circulation, infected seeds'
        },
        'powdery_mildew': {
            'description': 'Fungal disease creating white powdery coating',
            'symptoms': 'White powdery spots on leaves, stunted growth',
            'causes': 'High humidity, poor air circulation, moderate temperatures'
        },
        'soybean_rust': {
            'description': 'Fungal disease causing rust-colored spots',
            'symptoms': 'Small rust-colored pustules on leaf undersides',
            'causes': 'Warm, humid weather conditions'
        },
        'charcoal_rot': {
            'description': 'Soil-borne fungal disease affecting roots and stems',
            'symptoms': 'Wilting, yellowing, black discoloration of stems',
            'causes': 'Hot, dry conditions, water stress, poor soil drainage'
        },
        'frogeye_leaf_spot': {
            'description': 'Fungal disease creating circular spots with light centers',
            'symptoms': 'Circular spots with gray centers and dark borders',
            'causes': 'Warm, humid conditions, infected crop residue'
        }
    }
    
    for disease, info in diseases.items():
        print(f"🔸 {disease.upper().replace('_', ' ')}")
        print(f"   Description: {info['description']}")
        print(f"   Symptoms: {info['symptoms']}")
        print(f"   Causes: {info['causes']}")
        print()


if __name__ == "__main__":
    try:
        interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check your setup and try again.")