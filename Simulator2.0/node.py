from collections import namedtuple
from network import Network
from connection import Connection
from chain import Chain
from consensus import Consensus
from simpy import *
from utils import *
from block import *
from message import *
import time
from scipy.stats import expon
# Maximum block hashes to keep in the known list (prevent DOS)
MAX_KNOWN_BLOCKS = 1024

Envelope = namedtuple('Envelope', \
                        'msg, \
                        timestamp, \
                        destination, \
                        origin')
class Node:
    nextNodeId = 0
    def __init__(self, 
                 env,
                 region: str, 
                 network: Network,
                 hashrate,
                 chain=None,
                 # processingTime, 
                 ):
        
        self.env = env
        self.region = region
        self.network = network
        self.hashrate = hashrate 
        self.block_generation_probability = 0
        self.consensus = Consensus(self.env)
        # self.processingTime = processingTime
        self.connecting = {}
        self.known_blocks = set()
        self.nid = Node.nextNodeId
        Node.nextNodeId += 1

        if chain == None:# if no chain as input, generate a base chain
            self.chain = Chain(self.env, self)
        else: 
            self.chain = chain
        # Join the node to the network
        self.network.add_node(self)
        self.env.data['block_propagation'].update({
            f'blocks propagation delay to node {self.nid}':
            {}})

    def find_block_generation_probability(self):
        """Find the block generation probability for this node.
            Use cdf of exponential distribution and the rate depends
            on the rate of hashrate and total_hash_rate
        """
        rate = self.hashrate/self.network.total_hashrate
        self.block_generation_probability = expon.cdf(rate)


    def build_new_block(self):
        """Builds a new candidate block and propagate it to the network
        We input in our model the block size limit, and also extrapolate the probability
        distribution for the number of transactions per block, based on measurements from
        the public network (https://www.blockchain.com/charts/n-transactions-per-block?timespan=2years).
        If the block size limit is 1 MB, as we know in Bitcoin, we take from the probability
        distribution the number of transactions, but if the user choose to simulate an
        environment with a 2 MB block, we multiply by two the number of transactions.
        With this we can see the performance in different block size limits."""
        
        prev_block = self.chain.head
        block_height = prev_block.height + 1
        miner = self.nid
        timestamp = self.env.now
        block_ntxs = get_random_values(\
            self.env.config["bitcoin"]["number_transactions_per_block"],\
            n=1)
        #difficulty = self.consensus.calc_difficulty(prev_block, timestamp)
        
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
        self.env.data['block_propagation'][
            f'blocks propagation delay to node {self.nid}'
            ].update({f'{candidate_block.hash}': 0})
        # Broadcast the new candidate block across the network
        new_blocks_msg = Message(self,[candidate_block])
        self.env.process(self.broadcast(new_blocks_msg))
        



    def connect(self, nodes: list):
        """Simulate an acknowledgement phase with given nodes. During simulation the nodes
            will have a channel."""
        for node in nodes:
            # Ignore when a node is trying to connect to itself
            if node.nid != self.nid:
                connection = Connection(self.env, self, node)

                # Set the bases to monitor the block & TX propagation
                # self.env.data['block_propagation'].update({
                #     f'{self.nid}_{node.nid}': {}})
                self.connecting[node.nid] = connection                 
                self.env.process(self._connecting(node, connection))

    def _connecting(self, node, connection):
        """Simulates the time needed to perform TCP handshake and acknowledgement phase.
        During the simulation we do not need to simulate it again.
        We consider that a node communicate with his peer using an open connection/channel
        during all the simulation."""
        #establish a connection and it takes some time
        origin_node = connection.origin_node
        destination_node = connection.destination_node
        latency = get_latency_delay(
            self.env, origin_node.region, destination_node.region)
        tcp_handshake_delay = 3*latency
        yield self.env.timeout(tcp_handshake_delay)
        self.env.process(destination_node.listening_node(connection))


    def _read_envelope(self, envelope):
        print(
            f'{self.nid} at \
            {datetime.utcfromtimestamp(self.env.now).strftime("%m-%d %H:%M:%S")}: \
            Receive a message (ID: {envelope.msg.id}) \
            created at {envelope.timestamp} \
            from {envelope.origin.nid}')


    def listening_node(self, connection):
        while True:
            # Get the messages from  connection
            envelope = yield connection.get()
            origin_region = envelope.origin.region
            dest_region = envelope.destination.region
            message_size = envelope.msg.size
            received_delay = get_received_delay(
                self.env, message_size, origin_region, dest_region)
            yield self.env.timeout(received_delay)

            # Track the time of knowing a block
            msg = envelope.msg
            if msg.id == 'blocks':
                blocks = {}
                for block in msg.blocks:
                    #the first time get a block
                    if block.hash not in self.known_blocks:
                        propagation_delay = self.env.now-block.timestamp
                        blocks.update({f'{block.hash}': propagation_delay})
                        self.env.data['block_propagation'][
                        f'blocks propagation delay to node {self.nid}'
                        ].update(blocks)
                        self.known_blocks.add(block.hash)
                        self.chain.add_block(block)
                        self.broadcast(msg)
                print(msg.size)
            self._read_envelope(envelope)


            # # Monitor the block propagation
            # if envelope.msg.id == 'blocks':
            #     block_propagation = self.env.data['block_propagation'][
            #         f'{envelope.origin.nid}_{envelope.destination.nid}']
            #     blocks = {}
            #     for block in envelope.msg.blocks:
            #         initial_time = block_propagation.get(f'{block.hash}', None)
            #         if initial_time is not None and :
            #             while len(self.known_blocks) >= MAX_KNOWN_BLOCKS:#NC
            #                 self.known_blocks.pop()
            #                  self.known_blocks[block_hash] = [self.env.now]
            #             propagation_time = self.env.now - initial_time
            #             blocks.update({f'{block.hash}': propagation_time})
                        # print(f'sent:{initial_time} received:{self.env.now}')
                # self.env.data['block_propagation']\
                #     [f'{envelope.origin.nid}_{envelope.destination.nid}'].update(blocks)

            

    def send(self, connection, msg): 
        """Send a message msg through connection"""
        origin_node = connection.origin_node
        destination_node = connection.destination_node

        upload_transmission_delay = get_sent_delay(
            self.env, msg.size, origin_node.region, destination_node.region)
        yield self.env.timeout(upload_transmission_delay)
        envelope = Envelope(msg, self.env.now,
            destination_node, origin_node)
        connection.put(envelope)

    def broadcast(self, msg):
        """Broadcast a message to all nodes with a channel"""
        for nid, connection in self.connecting.items():
            origin_node = connection.origin_node
            destination_node = connection.destination_node

            upload_transmission_delay = get_sent_delay(
                self.env, msg.size, origin_node.region, destination_node.region)
            yield self.env.timeout(upload_transmission_delay)
            envelope = Envelope(msg, self.env.now,
                destination_node, origin_node)
            connection.put(envelope)
                # self.send(connection,msg)
