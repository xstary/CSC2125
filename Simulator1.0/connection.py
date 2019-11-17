from simpy import *
from utils import *
class Connection:
    """This class represents the propagation through a Connection."""

    def __init__(self, env, origin_node, destination_node):
        self.env = env
        self.store = Store(env)
        self.origin_node = origin_node
        self.destination_node = destination_node

    def latency(self, envelope):
        latency_delay = get_latency_delay(
            self.env, self.origin_node.region, self.destination_node.region)
        yield self.env.timeout(latency_delay)
        self.store.put(envelope)

    def put(self, envelope):
        print(
            f'{envelope.origin.nid} at {envelope.timestamp}: \
            Message (ID: {envelope.msg.id}) \
            sent with {envelope.msg.size} MB\
            with a destination: {envelope.destination.nid}')
        self.env.process(self.latency(envelope))

    def get(self):
        return self.store.get()
