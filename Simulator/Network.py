import util
import random
class Network:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.blockchain = self.env.config['blockchain']
        self.total_hashrate = 0
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
            time_between_blocks = round(get_random_values(
                self.env.delays['time_between_blocks_seconds'])[0], 2)
            yield self.env.timeout(time_between_blocks)
            orphan_blocks_probability = self.env.config[self.blockchain]['orphan_blocks_probability']
            simulate_orphan_blocks = scipy.random.choice(
                [True, False], 1, p=[orphan_blocks_probability, 1-orphan_blocks_probability])[0]
            if simulate_orphan_blocks:
                selected_nodes = scipy.random.choice(
                    self._list_nodes, 2, replace=False, p=self._list_probabilities)
                for selected_node in selected_nodes:
                    self._build_new_block(selected_node)
            else:
                selected_node = scipy.random.choice(
                    self._list_nodes, 1, replace=False, p=self._list_probabilities)[0]
                self._build_new_block(selected_node)

    def _build_new_block(self, node):
        print(
            f'Network at {time(self.env)}: Node {node.nid} selected to broadcast his candidate block')
        # Give orders to the selected node to broadcast his candidate block
        node.mining()





