from utils import kB_to_MB

class Message:  
    """Defines a model for the network messages of the Bitcoin blockchain.
    For each message its calculated the size, taking into account measurements from the live and public network.
    """

    def __init__(self, sender, blocks=None):
        self.sender = sender
        if blocks != None:
            self.id = "blocks"
            self.blocks = blocks
            message_size = self.sender.env.config['bitcoin']['message_size_kB']
            total_block_size = 0
            for block in self.blocks:
                total_block_size = message_size['header'] + \
                                message_size['tx'] * block.ntxs + \
                                message_size['block_base']
            self.size = kB_to_MB(float(total_block_size))
        else:
            self.id = "non-block"
            self.blocks = None
            message_size = self.sender.env.config['bitcoin']['message_size_kB']['verack']# not sure what the verack is
            self.size = kB_to_MB(message_size)


    # def version(self):
    #     """ When a node creates an outgoing connection, it will immediately advertise its version.
    #     https://en.bitcoin.it/wiki/Protocol_documentation#version"""
    #     return {
    #         'id': 'version',
    #         'size': kB_to_MB(self._header_size + self._message_size['version'])
    #     }

    # def verack(self):
    #     """ The verack message is sent in reply to version. This message consists of only
    #     a message header with the command string "verack".
    #     https://en.bitcoin.it/wiki/Protocol_documentation#verack"""
    #     return {
    #         'id': 'verack',
    #         'size': kB_to_MB(self._header_size + self._message_size['verack'])
    #     }

    # def inv(self, hashes: list, _type: str):
    #     """Allows a node to advertise its knowledge of one or more transactions or blocks
    #     https://en.bitcoin.it/wiki/Protocol_documentation#inv"""
    #     num_items = len(hashes)
    #     inv_size = num_items * self._message_size['inv_vector']
    #     return {
    #         'id': 'inv',
    #         'type': _type,
    #         'hashes': hashes,
    #         'size': kB_to_MB(self._header_size + inv_size)
    #     }

    # def get_data(self, hashes: list, _type: str):
    #     """Used to retrieve the content of a specific type (e.g. block or transaction).
    #     It can be used to retrieve transactions or blocks
    #     https://en.bitcoin.it/wiki/Protocol_documentation#getdata"""
    #     num_items = len(hashes)
    #     inv_size = num_items * self._message_size['inv_vector']
    #     return {
    #         'id': 'getdata',
    #         'type': _type,
    #         'hashes': hashes,
    #         'size': kB_to_MB(self._header_size + inv_size)
    #     }
