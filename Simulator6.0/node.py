from collections import namedtuple
from network import Network
from chain import Chain
from consensus import *
from simpy import *
from utils import *
from block import *
from message import *
import time
from scipy.stats import expon
import numpy as np
import math
# Maximum block hashes to keep in the known list (prevent DOS)
MAX_KNOWN_BLOCKS = 1024

class Node:
    nextNodeId = 0
    def __init__(self, 
                 network,
                 region: str,     
                 hashrate,
                 chain=None,
                 # processingTime, 
                 ):

        self.region = region
        self.network = network
        self.hashrate = hashrate 
        self.block_generation_probability = 0
        # self.processingTime = processingTime
        self.neighbours = {}
        self.known_blocks = set()
        self.nid = Node.nextNodeId
        Node.nextNodeId += 1

        if chain == None:# if no chain as input, generate a base chain
            self.chain = Chain(self)
        else: 
            self.chain = chain
        # Join the node to the network
        self.network.add_node(self)
        self.network.data['block_propagation'].update({
            f'blocks propagation delay to node {self.nid}':
            {}})

    def connect(self, nodes: list):
        nconnection = int(get_random_values(self.network.number_of_connections,1))
        # print(f'{self.network.number_of_connections} dis')
        # nconnection = int(np.random.normal(2, 0.5,1)[0])
        if nconnection >= len(nodes):
            selected_nodes = nodes
        else:
            selected_nodes = random.sample(nodes, k=nconnection)
        print(f'{nconnection} connections')
        for node in selected_nodes:
            # Ignore when a node is trying to connect to itself
            if node.nid != self.nid:
                self.neighbours[node.nid] = node   

    def get_block_generation_time(self):
        if self.hashrate == 0:
            return None
        rate = self.hashrate/(10 * self.network.total_hashrate)
        #get block generation time in ms
        time = 60 * 1000 * expon.rvs(scale = 1/rate,size = 1)[0]
        return time

    def broadcast(self, simulator, msg):
        """Broadcast a message to all neighbours nodes"""
        for nid, node in self.neighbours.items():
            simulator.schedule_block_propogation_event(self, node, msg)


    def build_new_block(self, simulator):
        prev_block = self.chain.head
        block_height = prev_block.height + 1
        miner = self.nid
        timestamp = simulator.now
        block_ntxs = get_random_values(\
            self.network.config["bitcoin"]["number_transactions_per_block"],\
            n=1)
        
        candidate_block = Block(
            block_height,
            prev_block.hash,
            miner,
            timestamp,
            block_ntxs)

        print(
            f'{self.nid} at time \
            {datetime.utcfromtimestamp(timestamp).strftime("%m-%d %H:%M:%S")}: \
            New candidate block #{candidate_block.height} \
            created {candidate_block.hash}')
        # Add the candidate block to the chain of the miner node
        self.known_blocks.add(candidate_block.hash)
        self.chain.add_block(candidate_block)
        self.network.data['block_propagation'][
            f'blocks propagation delay to node {self.nid}'
            ].update({f'{candidate_block.hash}': 0})
        # Broadcast the new candidate block across the network
        new_blocks_msg = Message(self, [candidate_block])
        self.broadcast(simulator, new_blocks_msg)
    


    def receive_block(self, simulator, msg):
        print(f'{self.nid} at \
        {datetime.utcfromtimestamp(simulator.now).strftime("%m-%d %H:%M:%S")}: \
        Receive a {msg.id} message ) \
        from {msg.sender.nid}')

        # Track the time of knowing a block
        if msg.id == 'blocks':
            blocks = {}
            for block in msg.blocks:
                #the first time get a block
                if block.hash not in self.known_blocks:
                    propagation_delay = simulator.now-block.timestamp
                    blocks.update({f'{block.hash}': propagation_delay})
                    self.network.data['block_propagation'][
                    f'blocks propagation delay to node {self.nid}'
                    ].update(blocks)
                    self.known_blocks.add(block.hash)
                    self.chain.add_block(block)
                    self.broadcast(simulator, msg)
            

  
                
