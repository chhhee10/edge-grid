# Discovery + Market Protocol

Owns: peer discovery (Kademlia DHT) + sealed-bid auction (GossipSub pub/sub) via py-libp2p.

## Reference
Study [conduit](https://github.com/skorotkiewicz/conduit) (rust-libp2p) for the DHT + model-routing pattern — port the *pattern*, not the code (different language).

## Deliverable
- 4-5 node local/LAN network that can discover each other via Kademlia DHT.
- GossipSub topic for job broadcast + bid collection (see `../shared/schemas.md` for message shapes).
- Auction logic: collect bids for a fixed window, select winner (lowest price / best latency estimate).

## Day 1 TODO
- [ ] `pip install -r requirements.txt`, get py-libp2p running with 2 local nodes finding each other via DHT.
- [ ] Agree on job broadcast / bid schema with inference track (see `../shared/schemas.md`).

## Experiment owned
Auction convergence time as node count increases (3 → 5 nodes) — see `../docs/EXPERIMENTS.md`.
