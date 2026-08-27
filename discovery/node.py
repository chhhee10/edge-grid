"""
Edge Grid node: Kademlia DHT peer discovery + GossipSub job auction.

See ../shared/schemas.md for the job_broadcast / bid message shapes.
Reference pattern: https://github.com/skorotkiewicz/conduit (DHT + model routing)
"""

import json
import uuid
import trio

from multiaddr import Multiaddr
from libp2p import new_host
from libp2p.peer.peerinfo import info_from_p2p_addr
from libp2p.kad_dht import KadDHT, DHTMode
from libp2p.tools.anyio_service.context import background_trio_service

class EdgeGridNode:
    def __init__(self, peer_id: str, listen_port: int, bootstrap_addr: str | None = None):
        self.peer_id = peer_id
        self.listen_port = listen_port
        self.bootstrap_addr = bootstrap_addr

        self.listen_addr = Multiaddr(
            f"/ip4/127.0.0.1/tcp/{self.listen_port}"
        )
        self.host = new_host()
        self.dht = KadDHT(self.host, DHTMode.SERVER)
        # TODO: initialize libp2p host, Kademlia DHT, GossipSub pubsub

    async def start(self):
        async with self.host.run(listen_addrs=[self.listen_addr]):
            async with background_trio_service(self.dht):
            
                print(f"Node {self.peer_id} is listening on:")
                print(self.host.get_addrs())
    
                if self.bootstrap_addr:
                    peer_info = info_from_p2p_addr(
                        Multiaddr(self.bootstrap_addr)
                    )
    
                    print(f"Connecting to {peer_info.peer_id}...")
    
                    await self.host.connect(peer_info)
    
                    print(f"Connected to {peer_info.peer_id}")
    
                    await trio.sleep(2)
    
                    print(
                        f"DHT routing table size: "
                        f"{self.dht.get_routing_table_size()}"
                    )

                await trio.sleep_forever()
            
    
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
