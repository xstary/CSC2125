import time
from datetime import datetime
from simulator import Simulator
from json import dumps as dump_json
from nodeGenerator import NodeGenerator
from network import Network
from block import *

def write_report(network):
    with open('output/report.json', 'w') as f:
        f.write(dump_json(network.data,indent=4))


def report_node(network, nodes_list):
    for node in nodes_list:
        head = node.chain.head
        main_chain_list = node.chain.get_main_chain()
        print(head.height)
        
        key = f'{node.nid}_summary'
        network.data[key] = {
            'nid': node.nid,
            'region': node.region,
            'connections': list(node.neighbours.keys()),
            'hashrate': node.hashrate,
            'head_block_hash': f'{head.hash} #{head.height}',
            'number_of_total_known_blocks': len(node.known_blocks),
            'number_of_total_blocks_inchain': node.chain.block_counter,
            'number_of_blocks_on_main_chain': len(main_chain_list),
            'main_chain_list': main_chain_list
        }
        network.data['system summary'].update({
            'fork_rate':1-len(main_chain_list)/node.chain.block_counter})

        
def report_system_summary(network, simulator, nodes_list): 
    network.data['system summary']= {
                'start_simulation_time': datetime.utcfromtimestamp(
                    simulator.initial_time).strftime('%m-%d %H:%M:%S'),
                'end_simulation_time': datetime.utcfromtimestamp(
                    simulator.initial_time + simulator.end_time).strftime('%m-%d %H:%M:%S'),
                'number_of_nodes': len(nodes_list),
                'number_of_blocks': Block.nextBlockHash
            }

def run_model():
    now = 0  # Current time
    end = 3600 * 2 * 1000# 2h in seconds

    # Create the network
    network = Network(
        'Network 0.0',
        'configs/config.json',
        'configs/latency.json',
        'configs/throughput-rec.json',
        'configs/throughput-send.json',
        'configs/delays.json')


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

    node_generator = NodeGenerator(network)
    # Create all nodes
    nodes_list = node_generator.create_nodes(miners)
    for node in nodes_list:
        node.connect(nodes_list)

    s = Simulator(network, now, end)
    s.run()

    report_system_summary(network, s, nodes_list)
    report_node(network, nodes_list)
    write_report(network)


if __name__ == '__main__':
    run_model()

