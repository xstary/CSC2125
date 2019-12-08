from utils import kB_to_MB

class Message:  
    def __init__(self, sender, ty, blocks):
        self.sender = sender
        self.blocks = blocks

        message_size = self.sender.network.config['bitcoin']['message_size_kB']

        if ty == "blocks":
            self.id = "blocks"
            total_block_size = 0
            for block in self.blocks:
                total_block_size = message_size['header'] + \
                                block.size + \
                                message_size['block_base']
            self.size = kB_to_MB(float(total_block_size))
        else:  
            # used to retrieve the content of a specific type (e.g. inv, get_data or block).
            if ty == "get_data":
                self.id = "get_data"
            # allows a node to advertise its knowledge of one or more blocks
            elif ty == "inv":
                self.id = "inv"
            num_items = len(blocks)
            message_size = message_size['header']+ num_items * message_size['inv_vector']
            self.size = kB_to_MB(message_size)
           


