import random
from node import *

class NodeGenerator:
    def __init__(self, network):
        self.network = network

    def create_nodes(self, full_nodes):
        # Unique ID for each node
        # Create the full nodes
        nodes_list = []
        for node_location, _nodes in full_nodes.items():
            for i in range(_nodes['how_many']):
                new = Node( self.network,
                            node_location,
                            0,
                            chain=None
                            )
                nodes_list.append(new)
        print(f'NodeGenerator: Created {len(nodes_list)} full nodes')
        return nodes_list
        
    def add_miner(self, miners):
        # Unique ID for each node
        # Create the miners nodes
        miners_list = []
        for name, info in miners.items():    
            hashrate= info["mega_hashrate"]
            miner_location = info["region"]

            new = Node( self.network,
                        miner_location,
                        hashrate,
                        info=name
                        )
            miners_list.append(new)
                

        print(f'NodeGenerator: Created {len(miners_list)} miners')
        return miners_list

    def _check_location(self, miners):
        nodes_location = list(miners.keys())
        for location in nodes_location:
            if location not in self._world.locations:
                raise RuntimeError(
                    f'There are not measurements for the location {location}. \
                    Only available locations: {self.network.locations()}')

