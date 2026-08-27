import trio

from libp2p import new_host
from libp2p.kad_dht import KadDHT, DHTMode
from libp2p.peer.id import ID
from libp2p.peer.peerinfo import info_from_p2p_addr
from libp2p.tools.anyio_service.context import background_trio_service
from multiaddr import Multiaddr


NODE1_ADDR = (
    "/ip4/127.0.0.1/tcp/4001/"
    "p2p/12D3KooWAuztxHq2DwQvLaPUxpZoqesLVzBKfKem2c7gHRcdiuwC"
)

NODE2_ID = (
    "12D3KooWJ5JSW9hKG1Uuy2ePfikqpspsqBP3voj2BiSjAsHmGsZ5"
)


async def main():
    host = new_host()

    async with host.run(
        listen_addrs=[Multiaddr("/ip4/127.0.0.1/tcp/0")]
    ):
        dht = KadDHT(host, DHTMode.SERVER)

        async with background_trio_service(dht):

            # Connect to Node 1
            peer_info = info_from_p2p_addr(
                Multiaddr(NODE1_ADDR)
            )

            print("Connecting to Node 1...")
            await host.connect(peer_info)
            print("Connected.")

            print(
                "Routing table:",
                dht.get_routing_table_size()
            )

            # Ask DHT to find Node 2
            target_peer_id = ID.from_string(NODE2_ID)

            print("Asking DHT to find Node 2...")

            result = await dht.find_peer(target_peer_id)

            if result:
                print("DHT DISCOVERY SUCCESS")
                print("Found Node 2:", result.peer_id)

                print("Node 2 addresses:")
                for addr in result.addrs:
                    print(" ", addr)

            else:
                print("DHT DISCOVERY FAILED")

            await trio.sleep_forever()


trio.run(main)