# Shared message schemas

The single most common integration break point on a project like this is the P2P layer and the inference layer disagreeing on message shape. Define it here first, and have both track owners agree on it on Day 1 before writing code against it.

## Job broadcast (discovery → all peers, via GossipSub)
```json
{
  "job_id": "uuid",
  "prompt": "string",
  "model": "qwen2.5:1.5b",
  "max_tokens": 256,
  "requester_peer_id": "string",
  "timestamp": 0
}
```

## Bid (peer → requester, via GossipSub or direct stream)
```json
{
  "job_id": "uuid",
  "bidder_peer_id": "string",
  "price": 0.0,
  "estimated_latency_ms": 0
}
```

## Inference result (winning peer → requester, via direct P2P stream)
```json
{
  "job_id": "uuid",
  "output": "string",
  "tokens_generated": 0,
  "latency_ms": 0,
  "output_hash": "sha256 hex string"
}
```

## Validation verdict (validator → local ledger)
```json
{
  "job_id": "uuid",
  "verdict": "pass | fail",
  "judge_score": 0.0,
  "reason": "string"
}
```

## Settlement record (local simulated ledger — contracts/ track)
```json
{
  "job_id": "uuid",
  "provider_peer_id": "string",
  "amount": 0.0,
  "slashed": false
}
```

Update this file the moment any track changes a field — don't let schemas drift silently between tracks.
