"""
Ollama Local Environment Setup & Verification Script
This script verifies that the local Ollama service is running and checks
for available quantized models (e.g. llama3.2:3b, phi3:mini).
No internet connectivity is required.
"""

import sys
import json
import urllib.request
import urllib.error

OLLAMA_BASE_URL = "http://localhost:11434"

def check_ollama_status():
    print("🔍 Checking local Ollama service status...")
    try:
        req = urllib.request.Request(f"{OLLAMA_BASE_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                models = [m.get("name") for m in data.get("models", [])]
                print(f"✅ Ollama service is RUNNING at {OLLAMA_BASE_URL}")
                print(f"📦 Installed local models ({len(models)}):")
                for m in models:
                    print(f"   - {m}")
                return models
    except urllib.error.URLError as e:
        print(f"❌ Could not connect to Ollama at {OLLAMA_BASE_URL}: {e.reason}")
        print("\n💡 Troubleshooting:")
        print("   1. Install Ollama from https://ollama.com")
        print("   2. Run 'ollama serve' or open the Ollama application")
        print("   3. Pull a model locally: 'ollama pull llama3.2:3b' or 'ollama pull phi3:mini'")
        return []
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return []

def test_inference(model_name: str):
    print(f"\n🧪 Testing local offline inference with model '{model_name}'...")
    payload = {
        "model": model_name,
        "prompt": "Respond with JSON: {\"status\": \"ok\", \"message\": \"Offline LLM ready\"}",
        "stream": False,
        "format": "json"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            print(f"✅ Model Response received:")
            print(f"   {result.get('response', '').strip()}")
            return True
    except Exception as e:
        print(f"❌ Inference test failed for {model_name}: {e}")
        return False

if __name__ == "__main__":
    models = check_ollama_status()
    if models:
        target_model = None
        for preferred in ["llama3.2:3b", "llama3.2", "phi3:mini", "phi3"]:
            matching = [m for m in models if preferred in m]
            if matching:
                target_model = matching[0]
                break
        if not target_model and models:
            target_model = models[0]
            
        if target_model:
            test_inference(target_model)
        else:
            print("\n⚠️ No preferred models found. Please pull 'llama3.2:3b' or 'phi3:mini'.")
    else:
        sys.exit(1)
