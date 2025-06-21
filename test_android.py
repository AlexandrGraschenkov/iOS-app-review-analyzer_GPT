#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.load_android_app_info import load_android_app_info
from utils.load_android_reviews import load_android_reviews

def test_android_functionality():
    print("Testing Android app info and reviews loading...")
    
    # Test with WhatsApp (a popular Android app)
    app_id = "com.smilesolutionteam.engquiz"
    
    print(f"\n1. Loading app info for {app_id}...")
    app_info = load_android_app_info(app_id)
    
    if app_info and "name" in app_info:
        print(f"✅ App info loaded successfully!")
        print(f"   Name: {app_info['name']}")
        print(f"   Developer: {app_info.get('developer', 'N/A')}")
        print(f"   Genre: {app_info.get('genre', 'N/A')}")
        print(f"   Score: {app_info.get('score', 'N/A')}")
        print(f"   Installs: {app_info.get('installs', 'N/A')}")
    else:
        print("❌ Failed to load app info")
        return False
    
    print(f"\n2. Loading reviews for {app_id}...")
    reviews = load_android_reviews(app_id, countries=["us", "gb"])
    
    if reviews and len(reviews) > 0:
        print(f"✅ Reviews loaded successfully!")
        print(f"   Total reviews: {len(reviews)}")
        print(f"   Sample review:")
        sample_review = reviews[0]
        print(f"     Author: {sample_review['author']}")
        print(f"     Rating: {sample_review['rating']}")
        print(f"     Content: {sample_review['content'][:100]}...")
    else:
        print("❌ Failed to load reviews")
        return False
    
    print("\n✅ Android functionality test completed successfully!")
    return True

if __name__ == "__main__":
    test_android_functionality() 