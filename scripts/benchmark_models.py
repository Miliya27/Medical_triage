"""
Offline Model Benchmarking Utility
Compares response latency, throughput, and structured JSON parsing accuracy
between Ollama models (llama3.2:3b vs phi3:mini).
"""

import time
import json
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/generate"

SAMPLE_SYMPTOMS = """
Patient is a 34-year-old male with sudden onset of severe shortness of breath, wheezing, 
and hives across upper torso after being stung by a bee 15 minutes ago.
Blood Pressure: 85/50, Heart Rate: 125 bpm, SpO2: 89%.
"""

def benchmark_model(model_name: str):
    print(f"\n⏱️ Benchmarking model: {model_name}")
    prompt = f"""You are an offline emergency medical symptom analyzer agent.
Analyze the following patient symptoms:
{SAMPLE_SYMPTOMS}

Respond ONLY with valid JSON matching this schema:
{{
  "suspected_conditions": ["condition 1", "condition 2"],
  "primary_concerns": ["concern 1"],
  "urgency_level": "RED" | "YELLOW" | "GREEN",
  "rationale": "short explanation"
}}
"""
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    start_time = time.time()
    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            elapsed = time.time() - start_time
            body = json.loads(resp.read().decode())
            response_text = body.get("response", "")
            parsed = json.loads(response_text)
            print(f"✅ Success! Latency: {elapsed:.2f} seconds")
            print(f"📄 Output JSON:\n{json.dumps(parsed, indent=2)}")
            return {"model": model_name, "latency": elapsed, "status": "SUCCESS", "parsed": parsed}
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Benchmarking failed for {model_name} after {elapsed:.2f}s: {e}")
        return {"model": model_name, "latency": elapsed, "status": "FAILED", "error": str(e)}

if __name__ == "__main__":
    print("=== Offline Multi-Agent LLM Benchmark ===")
    results = []
    for model in ["llama3.2:3b", "phi3:mini"]:
        results.append(benchmark_model(model))
    
    print("\n=== Benchmark Summary ===")
    for r in results:
        print(f"Model: {r['model']:<15} | Status: {r['status']:<8} | Latency: {r.get('latency', 0):.2f}s")
