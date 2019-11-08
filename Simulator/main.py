import time
from json import dumps as dump_json
from world import SimulationWorld
from node_factory import NodeFactory
from blocksim.models.network import Network


def write_report(world):
    with open('output/report.json', 'w') as f:
        f.write(dump_json(world.env.data))


def report_node_chain(world, nodes_list):
    for node in nodes_list:
        head = node.chain.head
        chain_list = []
        num_blocks = 0
        for i in range(head.height):
            b = node.chain.get_block_by_height(i)
            chain_list.append(str(b.header))
            num_blocks += 1
        chain_list.append(str(head.header))
        key = f'{node.nid}_chain'
        world.env.data[key] = {
            'head_block_hash': f'{head.hash[:8]} #{head.height}',
            'number_of_blocks': num_blocks,
            'chain_list': chain_list
        }


def run_model():
    now = int(time.time())  # Current time
    duration = 3600  # seconds

    world = SimulationWorld(
        duration,
        now,
        'input-parameters/config.json',
        'input-parameters/latency.json',
        'input-parameters/throughput-received.json',
        'input-parameters/throughput-sent.json',
        'input-parameters/delays.json')

    # Create the network
    network = Network(world.env, 'NetworkXPTO')

    miners = {
        'Ohio': {
            'how_many': 0,
            'mega_hashrate_range': "(20, 40)"
        },
        'Tokyo': {
            'how_many': 2,
            'mega_hashrate_range': "(20, 40)"
        }
        'Tokyo': {
            'how_many': 1
        },
        'Ireland': {
            'how_many': 1
    }


    node_factory = NodeFactory(world, network)
    # Create all nodes
    nodes_list = node_factory.create_nodes(miners)
    # Start the network heartbeat
    world.env.process(network.start_heartbeat())
    # Full Connect all nodes
    for node in nodes_list:
        node.connect(nodes_list)

    world.start_simulation()

    report_node_chain(world, nodes_list)
    write_report(world)


if __name__ == '__main__':
    run_model()

