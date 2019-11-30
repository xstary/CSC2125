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


def report_node(world, nodes_list):
    for node in nodes_list:
        head = node.chain.head
        main_chain_list = node.chain.get_main_chain()
        print(head.height)
        
        key = f'{node.nid}_summary'
        world.env.data[key] = {
            'nid': node.nid,
            'region': node.region,
            'connections': list(node.connecting.keys()),
            'hashrate': node.hashrate,
            'head_block_hash': f'{head.hash} #{head.height}',
            'number_of_total_known_blocks': len(node.known_blocks),
            'number_of_total_blocks_inchain': node.chain.block_counter,
            'number_of_blocks_on_main_chain': len(main_chain_list),
            'main_chain_list': main_chain_list
        }
        world.env.data['system summary'].update({
            'fork_rate':1-len(main_chain_list)/node.chain.block_counter})

        
def report_system_summary(world, nodes_list): 
    world.env.data['system summary']= {
                'start_simulation_time': datetime.utcfromtimestamp(
                    world._initial_time).strftime('%m-%d %H:%M:%S'),
                'end_simulation_time': datetime.utcfromtimestamp(
                    world._initial_time + world._sim_duration).strftime('%m-%d %H:%M:%S'),
                'number_of_nodes': len(nodes_list),
                'number_of_blocks': Block.nextBlockHash,
            }

def run_model():
    now = 0  # Current time
    duration = 3600 * 2 # 1h in seconds

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
        'America': {
            'how_many': 1,
            'mega_hashrate_range': (20, 40)
        },
        'Asia': {
            'how_many': 2,
            'mega_hashrate_range': (30, 50)
        },
        'Europe': {
            'how_many': 1,
            'mega_hashrate_range': (0, 20)
        }
    }

    node_generator = NodeGenerator(world, network)
    # Create all nodes
    nodes_list = node_generator.create_nodes(miners)
    # Start the network heartbeat
    world.env.process(network.start_heartbeat())
    # Set the block generation prbability according to 
    # total hashrate in the network and connect nodes
    for node in nodes_list:
        node.find_block_generation_probability()
        node.connect(nodes_list)

    world.start_simulation()

    report_system_summary(world, nodes_list)
    report_node(world, nodes_list)
    write_report(world)


if __name__ == '__main__':
    run_model()

