import random
import itertools
from blocksim.utils import time


class Chain:
    """Defines a base chain model that needs to be extended according to blockchain protocol
    being simulated"""

    def __init__(self, env, node, consensus, genesis, db):
        self.env = env
        self.node = node
        self.consensus = consensus
        self.db = db
        self.genesis = genesis

        # # Set the score (AKA total difficulty in PoW)
        # self.db.put(f'score:{genesis.hash}', "0")

        # Init the chain with the Genesis block
        self.db.put(f'block:{genesis.height}', genesis.hash)
        self.db.put(genesis.hash, genesis)
        self._head_hash = genesis.hash
        self.parent_queue = {}


    def head(self):
        """Block in the head (tip) of the chain"""
        block = self.db.get(self._head_hash)
        return block

    def get_parent(self, block):
        """Genesis Block do not have parent"""
        if block.height == 0:
            return None
        return self.get_block(block.parentHash)

    def get_block(self, hash):
        """Gets the block with a given block hash"""
        try:
            return self.db.get(hash)
        except BaseException:
            return None

    def get_block_hash_by_height(self, height):
        """Gets the hash of the block with the given block number"""
        try:
            return self.db.get(f'block:{height}')
        except BaseException:
            return None

    def get_block_by_height(self, height):
        """Gets the block with the given block number"""
        #will there be multiple blocks at the same height??
        return self.get_block(self.get_block_hash_by_height(height))

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
                'child:' + child.parentHash,
                existing + child.hash)

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

    # def get_pow_difficulty(self, block):
    # NC ??? why do we need block difficulty for simulation
    #     """Get the total difficulty in PoW of a given block"""
    #     if not block:
    #         return 0
    #     key = f'score:{block.hash}'
    #     fills = []
    #     while key not in self.db:
    #         fills.insert(0, (block.hash, block.difficulty))
    #         key = f'score:{block.prevhash}'
    #         block = self.get_parent(block)
    #         if block is None:
    #             return 0
    #     score = int(self.db.get(key))
    #     for h, d in fills:
    #         key = f'score:{h}'
    #         score = score + d + random.randrange(10**6 + 1)
    #         self.db.put(key, str(score))
    #     return score

    def get_children(self, block):
        """Get the children of a block"""
        return [self.get_block(h) for h in self.get_child_hashes(block.hash)]

    def add_block(self, block):
        # NC ???
        """Call upon receiving a block"""
        # Is the block being added to the heap?
        if block.parentHash == self._head_hash:
            print(
                f'{self.node.nid} at {time(self.env)}: \
                Adding block #{block.height} ({block.hash[:8]}) to the head', )
            self.db.put(f'block:{block.height}', block.hash)
            self._head_hash = block.hash
        # Or is the block being added to a chain that is not currently the head?
        elif block.parentHash in self.db:
            print(
                f'{self.node.nid} at {time(self.env)}: \
                Receiving block #{block.height} ({block.hash[:8]}) \
                not on head ({self._head_hash[:8]}), \
                adding to secondary chain')
            key = f'forks_{self.node.nid}'
            self.env.data[key] += 1
            block_td = self.get_pow_difficulty(block)

            # If the block should be the new head, replace the head
            if block_td > self.get_pow_difficulty(self.head()):
                b = block
                new_chain = {}

                # Find common ancestor
                while b.height >= 0:
                    new_chain[b.height] = b
                    key = f'block:{b.height}'
                    orig_at_height = self.db.get(
                        key) if key in self.db else None
                    if orig_at_height == b.hash:
                        break
                    if b.parentHash not in self.db or self.db.get(
                            b.parentHash) == self.genesis.hash:
                        break
                    b = self.get_parent(b)
                replace_from = b.height
                # Replace block index 

                # Read: for i in range(common ancestor block number...new block
                # number)
                for i in itertools.count(replace_from):
                    print(
                        f'{self.node.address} at {time(self.env)}: Rewriting height {i}')
                    key = f'block:{i}'
                    # Delete data for old blocks
                    orig_at_height = self.db.get(
                        key) if key in self.db else None
                    if orig_at_height:
                        orig_block_at_height = self.get_block(orig_at_height)
                        print(
                            f'{self.node.address} at {time(self.env)}: \
                            {orig_block_at_height.hash} no longer in main chain')
                        # Delete from block index
                        self.db.delete(key)
                    # Add data for new blocks
                    if i in new_chain:
                        new_block_at_height = new_chain[i]
                        print(
                            f'{self.node.nid} at {time(self.env)}: \
                            {new_block_at_height.hash} now in main chain')
                        # Add to block index
                        self.db.put(key, new_block_at_height.hash)
                    if i not in new_chain and not orig_at_height:
                        break
                self._head_hash = block.hash
        # Block has no parent yet. An Orphan block
        else:
            if block.parentHash not in self.parent_queue:
                self.parent_queue[block.parentHash] = []
            self.parent_queue[block.parentHash].append(block)
            print(
                f'{self.node.nid} at {time(self.env)}: \
                Got block #{block.height} ({block.hash[:8]}) \
                with prevhash {block.parentHash[:8]}, \
                parent not found. Delaying for now')
            return False

        self.add_child(block)

        self.db.put(block.hash, block)

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
