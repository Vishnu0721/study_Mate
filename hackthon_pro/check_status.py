#!/usr/bin/env python3
"""
Status checker for the Document Analysis AI application
"""

import os
import requests
import time
from pathlib import Path

def check_model_cache():
    """Check if model files are being downloaded"""
    cache_dir = Path("./model_cache")
    if not cache_dir.exists():
        print("❌ Model cache directory not found")
        return False
    
    # Check for model files
    model_files = list(cache_dir.rglob("*.safetensors"))
    tokenizer_files = list(cache_dir.rglob("*.json"))
    
    if model_files:
        print(f"✅ Found {len(model_files)} model files")
        total_size = sum(f.stat().st_size for f in model_files)
        print(f"📊 Total model size: {total_size / (1024**3):.2f} GB")
        return True
    elif tokenizer_files:
        print("⏳ Model files are being downloaded...")
        return False
    else:
        print("❌ No model files found")
        return False

def check_flask_app():
    """Check if Flask app is running"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("✅ Flask application is running")
            return True
        else:
            print(f"⚠️ Flask app responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Flask application is not running")
        return False
    except Exception as e:
        print(f"❌ Error checking Flask app: {e}")
        return False

def main():
    print("🔍 Document Analysis AI - Status Check")
    print("=" * 50)
    
    # Check model cache
    print("\n📦 Model Status:")
    model_ready = check_model_cache()
    
    # Check Flask app
    print("\n🌐 Application Status:")
    app_running = check_flask_app()
    
    print("\n" + "=" * 50)
    if model_ready and app_running:
        print("🎉 Everything is ready! You can use the application.")
        print("🌐 Open: http://localhost:5000")
    elif app_running:
        print("⏳ Application is running but model is still downloading...")
        print("📊 This may take several minutes for the first time.")
    else:
        print("❌ Application is not ready yet.")
        print("💡 Make sure to run: python app.py")

if __name__ == "__main__":
    main() 