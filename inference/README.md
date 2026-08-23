# Edge Inference Engine

Owns: Ollama wrapper, hardware benchmarking, streaming inference results back over P2P.

## Deliverable
- Wrapper around Ollama (small quantized model: Qwen2.5-1.5B or Llama-3.2-3B) that runs on a laptop, no GPU required.
- Hardware benchmarking script (measure TTFT, tokens/sec on each team member's machine).
- Streams tokens/result back to requester (see `../shared/schemas.md` for the inference_result shape).

## Day 1 TODO
- [ ] Install [Ollama](https://ollama.com), pull the chosen model: `ollama pull qwen2.5:1.5b`
- [ ] `pip install -r requirements.txt`, get a basic prompt → completion round trip working.
- [ ] Agree on inference_result schema with discovery track.

## Experiment owned
Latency (TTFT) vs. hosted API baseline — see `../docs/EXPERIMENTS.md`.
