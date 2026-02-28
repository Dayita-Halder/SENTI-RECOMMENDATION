"""Quick test to verify model loading works"""
import os
print("Testing model loading...")
print(f"Current directory: {os.getcwd()}")

try:
    from model import get_system
    print("✓ Model module imported successfully")
    
    print("\nInitializing system...")
    system = get_system()
    print("✓ System initialized successfully!")
    
    # Test prediction
    test_review = "This product is amazing, I love it!"
    print(f"\nTesting prediction with: '{test_review}'")
    result = system.predict_sentiment(test_review)
    print(f"✓ Prediction result: {result}")
    
    print("\n✅ ALL TESTS PASSED! Model is working correctly.")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
