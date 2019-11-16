import time
from datetime import datetime
from json import dumps as dump_json
from world import SimulationWorld
from nodeGenerator import NodeGenerator
from network import Network
from block import *


def write_report(world):
    with open('output/report.json', 'w') as f:
        f.write(dump_json(world.env.data,indent=4))


def report_node_chain(world, nodes_list):
    for node in nodes_list:
        head = node.chain.head()
        chain_list = []
        num_blocks = 0
        for i in range(head.height):
            b = node.chain.get_block_by_height(i)
            chain_list.append(str(b.hash))
            num_blocks += 1
        chain_list.append(str(head.hash))

        key = f'{node.nid}_chain'
        world.env.data[key] = {
            'nid': node.nid,
            'region': node.region,
            'hashrate': node.hashrate,
            'head_block_hash': f'{head.hash} #{head.height}',
            'number_of_blocks': num_blocks,
            'chain_list': chain_list
        }
def report_system_summary(world, nodes_list): 
    world.env.data['system summary']= {
                'start_simulation_time': datetime.utcfromtimestamp(
                    world._initial_time).strftime('%m-%d %H:%M:%S'),
                'end_simulation_time': datetime.utcfromtimestamp(
                    world._initial_time + world._sim_duration).strftime('%m-%d %H:%M:%S'),
                'number_of_nodes': len(nodes_list),
                'number_of_blocks': Block.nextBlockHash
            }



def run_model():
    now = 0  # Current time
    duration = 3600  # 1h in seconds

    world = SimulationWorld(
        duration,
        now,
        'configs/config.json',
        'configs/latency.json',
        'configs/throughput-rec.json',
        'configs/throughput-send.json',
        'configs/delays.json')

    # Create the network
    network = Network(world.env, 'Network0.0')

    miners = {
        'Ohio': {
            'how_many': 1,
            'mega_hashrate_range': (20, 40)
        },
        'Tokyo': {
            'how_many': 2,
            'mega_hashrate_range': (30, 50)
        },
        'Ireland': {
            'how_many': 1,
            'mega_hashrate_range': (0, 20)
        }
    }

    node_generator = NodeGenerator(world, network)
    # Create all nodes
    nodes_list = node_generator.create_nodes(miners)
    # Start the network heartbeat
    world.env.process(network.start_heartbeat())
    # Full Connect all nodes
    for node in nodes_list:
        node.connect(nodes_list)

    world.start_simulation()

    report_node_chain(world, nodes_list)
    report_system_summary(world, nodes_list)
    write_report(world)


if __name__ == '__main__':
    run_model()

