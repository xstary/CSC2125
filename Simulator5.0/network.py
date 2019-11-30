from utils import *
import random
import numpy as np
import scipy

class Network:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.blockchain = self.env.config['blockchain']
        self.number_of_connections = self.env.config[self.blockchain]['nconnections']
        self.total_hashrate = 0
        self.difficulty = self.env.delays['time_between_blocks_seconds'] #the target block generation time
        self._nodes = {}
        self._list_nodes = []
        self._list_probabilities = []

    def get_node(self, nid):
        return self._nodes.get(nid)

    def add_node(self, node):
        self._nodes[node.nid] = node
        self.total_hashrate += node.hashrate

    def _init_lists(self):
        for nid, node in self._nodes.items():
            self._list_nodes.append(node)
            node_prob = node.hashrate / self.total_hashrate
            self._list_probabilities.append(node_prob)

    def start_heartbeat(self):
        """ The "heartbeat" frequency of any blockchain network 
        		based on PoW is time differenc between blocks. 
        	With this function we simulate the network heartbeat frequency.
        	During all the simulation, between time intervals 
        		(corresponding to the time between blocks)
        		its chosen 1 or 2 nodes to broadcast a candidate block.
        	We choose 2 nodes, 
        		when we want to simulate an orphan block situation.
        	A fork due to orphan blocks occurs 
        		when there are two equally or nearly equally
        		valid candidates for the next block of data in the blockchain. 
        	This event can occur
        		when the two blocks are found close in time, 
        		and are submitted to the network at different “ends”.
        	Each node has a corresponding hashrate. 
        	The greater the hashrate, 
        		the greater the probability of the node being chosen.
        """
        self._init_lists()
        while True:
            successful_nodes = []
            for node in self._list_nodes:
                print(f'node.block_generation_probability:{node.block_generation_probability}')
                print(f'rate:{node.hashrate/self.total_hashrate}')
                if scipy.random.choice(
                 [True, False], 1, 
                 p=[node.block_generation_probability, 
                 1-node.block_generation_probability])[0]:
                    successful_nodes.append(node)

            # print(f'para:{self.env.delays}')
            # print(f'env time 1: {self.env.now}')
            time_between_blocks = round(get_random_values(
                self.env.delays['time_between_blocks_seconds'])[0], 4)
            # print(f'time_between_blocks {time_between_blocks}')


            close_time_between_blocks = scipy.stats.norm.rvs(loc=time_between_blocks, scale=10, size=len(successful_nodes))
            close_time_between_blocks = np.sort(close_time_between_blocks)
            for i in range(len(successful_nodes)):
                if i == 0:
                    time_diff = close_time_between_blocks[0]
                else:
                    time_diff = close_time_between_blocks[i]- close_time_between_blocks[i-1]
                print(close_time_between_blocks)
                # print(f'block interval: {time_diff}')
                yield self.env.timeout(time_diff)
                # print(f'env time {self.env.now}')
                self._build_new_block(node)

    def _build_new_block(self, node):
        print(
            f'Network at {time(self.env)}: Node {node.nid} selected to broadcast his candidate block')
        # Give orders to the selected node to broadcast his candidate block
        node.build_new_block()





