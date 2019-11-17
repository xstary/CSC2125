import random
import itertools
import time
from db import *
from block import Block


class Chain:
    """Defines a base chain model that needs to be extended according to blockchain protocol
    being simulated"""
    def __init__(self, env, node):
        self.env = env
        self.node = node
        self.db = BaseDB()
        self.current_height = 0
        self.block_counter = 0
        

        # Set the score (AKA total difficulty in PoW)
        # self.db.put(f'score:{genesis.hash}', "0")

        # Init the chain with the Genesis block
        if Block.genesis == None:
            genesis = Block(0, None, self.node, self.env.now, 0)
            Block.set_genesis(genesis)

        self.genesis = Block.genesis
        node.known_blocks.add(self.genesis.hash)
        # main chain
        # self.db.put(f'height:{self.genesis.height}', self.genesis.hash)
        #keep track blocks at each height: if there is more than one
        #block at a height, then there is a fork

        self.db.put(self.current_height,[self.genesis])
        self.db.put(f'{self.genesis.hash}', self.genesis)
        self.block_counter += 1

        self.head = self.genesis
        self.parent_queue = {}

    def get_main_chain(self):
        cur = self.head
        chain_list = []
        while cur.height > 0:
            chain_list.append(f'{cur.hash}')
            cur = self.get_parent(cur)
        chain_list.append(f'{cur.hash}')
        return chain_list



    def get_parent(self, block):
        """Genesis Block do not have parent"""
        if block.height == 0:
            return None
        return self.get_block(block.parentHash)

    def get_block(self, bhash):
        """Gets the block with a given block hash"""
        try:
            return self.db.get(f'{bhash}')
        except BaseException:
            return None
            

    def get_block_by_height(self, height):
        """Gets the block on main chain
        with the given block number"""
        cur = self.head
        if height > cur.height:
            return None
        while height < cur.height:
            print(cur.height)
            cur = self.get_parent(cur)
        return cur


    def get_block_hash_by_height(self, height):
        """Gets the hash of the block on main chain
        with the given block number"""
        try:
            return self.get_block_by_height(height).hash
        except BaseException:
            return None

    def add_child(self, child):
        """Add a record allowing you to later look up the provided block's
        parent hash and see that it is one of its children"""
        ## NC ????
        try:
            existing = self.db.get('child:' + child.parentHash)
        except BaseException:
            existing = ''
        existing_hashes = []
        for i in range(0, len(existing), 32):
            existing_hashes.append(existing[i: i + 32])
        if child.hash not in existing_hashes:
            self.db.put(
                'child:' + str(child.parentHash),
                existing + str(child.hash))

    def get_child_hashs(self, hash):
        """Get the hashes of all known children of a given block"""
        child_hashs = []
        try:
            data = self.db.get('child:' + hash)
            for i in range(0, len(data), 32):
                child_hashs.append(data[i:i + 32])
            return child_hashs
        except BaseException:
            return []


    def get_children(self, block):
        """Get the children of a block"""
        return [self.get_block(h) for h in self.get_child_hashes(block.hash)]

    def add_block(self, block):
        """Call upon receiving new a block"""
        # Double check the block is not in the chain
        key = f'{block.hash}'
        if key in self.db:
            return 
            
        # The block being added to a fork
        pkey = f'{block.parentHash}'
        if pkey in self.db:
            self.db.put(key,block)
            self.block_counter += 1
        
            if block.height > self.head.height:
                self.head = block
                self.db.put(block.height, [block])
                # self.db.put(f'height:{block.height}', block.hash)
                print(
                f'{self.node.nid} at {self.env.now}: \
                # Adding block #{block.height} ({block.hash}) to the head')
            else:
                l = self.db.get(block.height)
                l.append(block)
                self.db.put(block.height,l)
                print(
                f'{self.node.nid} at {self.env.now}: \
                # Adding block #{block.height} ({block.hash}) to a fork')

            if block.hash in self.parent_queue:
                for blk in self.parent_queue[block.hash]:
                    self.add_block(blk)
        
        # Block has no parent yet
        else:
            if block.parentHash not in self.parent_queue:
                self.parent_queue[block.parentHash] = []
            self.parent_queue[block.parentHash].append(block)
            print(
                f'{self.node.nid} at {time(self.env)}: \
                Got block #{block.height} ({block.hash}) \
                with prevhash {block.parentHash}, \
                parent not found. Delaying for now')
            return False

        self.add_child(block)


        # Are there blocks that we received that were waiting for this block?
        # If so, process them.
        if block.hash in self.parent_queue:
            for _block in self.parent_queue[block.hash]:
                self.add_block(_block)
            del self.parent_queue[block.hash]
        return True


    def __contains__(self, block):
        try:
            o = self.get_block_hash_by_height(block.height)
            assert o == block.hash
            return True
        except Exception as e:
            return False

    def get_block_hashes_from_hash(self, block_hash, max_num):
        """Get blockhashes starting from a hash and going backwards"""
        block = self.get_block(block_hash)
        if block is None:
            return []
        hashes = []
        hashes.append(block.hash)
        for i in range(max_num - 1):  # We already have one block added to the hashes list
            block = self.get_block(block.parentHash)
            if block is None:
                break
            hashes.append(block.hash)
            if block.height == 0:
                break
        return hashes
