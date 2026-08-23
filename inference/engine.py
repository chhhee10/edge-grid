"""
Edge inference engine: wraps Ollama, benchmarks hardware, produces inference_result messages.

See ../shared/schemas.md for the inference_result shape.
"""

import hashlib
import time

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


class InferenceEngine:
    def __init__(self, model: str = "qwen2.5:1.5b"):
        self.model = model

    def run(self, job_id: str, prompt: str, max_tokens: int = 256) -> dict:
        start = time.monotonic()
        response = requests.post(
            OLLAMA_URL,
            json={"model": self.model, "prompt": prompt, "stream": False, "options": {"num_predict": max_tokens}},
            timeout=120,
        )
        response.raise_for_status()
        latency_ms = (time.monotonic() - start) * 1000
        output = response.json()["response"]

        return {
            "job_id": job_id,
            "output": output,
            "tokens_generated": len(output.split()),  # TODO: use real token count from Ollama response
            "latency_ms": latency_ms,
            "output_hash": hashlib.sha256(output.encode()).hexdigest(),
        }


def benchmark_hardware(engine: InferenceEngine, prompt: str = "Explain gravity in one sentence.") -> dict:
    # TODO: run N trials, report TTFT mean/median/p95, log CPU/RAM via psutil
    raise NotImplementedError


if __name__ == "__main__":
    engine = InferenceEngine()
    result = engine.run(job_id="test", prompt="Explain gravity in one sentence.")
    print(result)
