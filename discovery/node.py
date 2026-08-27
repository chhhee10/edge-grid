"""
Edge Grid node: Kademlia DHT peer discovery + GossipSub job auction.

See ../shared/schemas.md for the job_broadcast / bid message shapes.
Reference pattern: https://github.com/skorotkiewicz/conduit (DHT + model routing)
"""

import json
import uuid


class EdgeGridNode:
    def __init__(self, peer_id: str, listen_port: int):
        self.peer_id = peer_id
        self.listen_port = listen_port
        # TODO: initialize libp2p host, Kademlia DHT, GossipSub pubsub

    async def start(self):
        # TODO: start libp2p host, join DHT, subscribe to job topic
        raise NotImplementedError

    async def broadcast_job(self, prompt: str, model: str, max_tokens: int = 256) -> str:
        job_id = str(uuid.uuid4())
        message = {
            "job_id": job_id,
            "prompt": prompt,
            "model": model,
            "max_tokens": max_tokens,
            "requester_peer_id": self.peer_id,
            "timestamp": 0,
        }
        # TODO: publish `message` (json.dumps) to the job GossipSub topic
        return job_id

    async def collect_bids(self, job_id: str, window_seconds: float = 2.0) -> list[dict]:
        # TODO: listen on bid topic for `window_seconds`, filter by job_id
        raise NotImplementedError

    def select_winner(self, bids: list[dict]) -> dict:
        return min(bids, key=lambda b: b["price"])


if __name__ == "__main__":
    # TODO: parse CLI args (peer_id, port, bootstrap peers), run node
    pass
