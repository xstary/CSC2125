import time
from datetime import datetime
from simulator import Simulator
from json import dumps as dump_json
from nodeGenerator import NodeGenerator
from network import Network
from block import *

def write_report(network,simulator, duration):
    print("rep")

    with open(f'output/nodes_{duration}h.json', 'w') as f:
        f.write(dump_json(network.data,indent=4))   

    with open(f'output/block_propogation_{duration}h.json', 'w') as f:
        f.write(dump_json(network.block_propagation,indent=4))

    with open(f'output/final_propagation_time_{duration}h.json', 'w') as f:
        f.write(dump_json(network.final_propagation_time,indent=4))

    with open(f'output/system_{duration}h.json', 'w') as f:
        f.write(dump_json(simulator.data,indent=4))



def report_node(network, simulator):
    nodes = simulator.network.nodes
    head0 = None
    simulator.data['system summary'].update({
        'fork_rate':0})
    for nid, node in nodes.items():
        head = node.chain.head
        if head.hash == head0:
            main_chain_list = f'same chain as node {0}'
        else:
            head0 = head.hash
            main_chain_list = node.chain.get_main_chain()
            fr = 1-len(main_chain_list)/node.chain.block_counter
            if fr > simulator.data['system summary']['fork_rate']:
                simulator.data['system summary'].update({
                    'fork_rate': fr})

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

        

        
def report_system_summary(simulator, nodes_list): 
    average_block_propa_time = 0
    count = 0
    for nid, t in simulator.network.final_propagation_time.items():
        average_block_propa_time += t
        count += 1
    average_block_propa_time = average_block_propa_time/count
    simulator.data['system summary']= {
                'start_simulation_time': datetime.utcfromtimestamp(
                    simulator.initial_time).strftime('%m-%d %H:%M:%S'),
                'end_simulation_time': datetime.utcfromtimestamp(
                   (simulator.initial_time + simulator.end_time)/1000).strftime('%m-%d %H:%M:%S'),
                'number_of_nodes': len(nodes_list),
                'number_of_blocks': Block.nextBlockHash,
                'average_block_propagation_time': average_block_propa_time
            }

def run_model(duration,now=0,):
    end = duration * 60 * 60 * 1000 #convert from h to ms
    # Create the network
    network = Network(
        'Network 0.0',
        'configs/config.json',
        'configs/latency.json',
        'configs/throughput-rec.json',
        'configs/throughput-send.json',
        'configs/delays.json')

    node_distribution =  network.config[network.blockchain]["node_distribution"]
    total_nodes = network.config[network.blockchain]["number_of_nodes"]

    full_nodes = {
        'NORTH_AMERICA': {
            'how_many': int(total_nodes*node_distribution['NORTH_AMERICA']),
            'mega_hashrate_range': (0, 0)
        },
        'SOUTH_AMERICA': {
            'how_many': int(total_nodes*node_distribution['SOUTH_AMERICA']),
            'mega_hashrate_range': (0, 0)
        },
        'ASIA_PACIFIC': {
            'how_many': int(total_nodes*node_distribution[ 'ASIA_PACIFIC']),
            'mega_hashrate_range': (0, 0)
        },
        'JAPAN': {
            'how_many': int(total_nodes*node_distribution['JAPAN']),
            'mega_hashrate_range': (0, 0)
        },
        'AUSTRALIA': {
            'how_many': int(total_nodes*node_distribution['AUSTRALIA']),
            'mega_hashrate_range': (0, 0)
        },
        'EUROPE': {
            'how_many': int(total_nodes*node_distribution['EUROPE']),
            'mega_hashrate_range': (0, 0)
        }
    }

    miners = network.config[network.blockchain]["mining_pool"]

    node_generator = NodeGenerator(network)
    nodes_list = node_generator.create_nodes(full_nodes)
    miner_list = node_generator.add_miner(miners)
    nodes_list.extend(miner_list)

    for node in nodes_list:
        node.connect(nodes_list)

    s = Simulator(network, now, end)
    s.run()

    report_system_summary(s, nodes_list)
    report_node(network, s)
    write_report(network,s,duration)


if __name__ == '__main__':
    b = time.time()
    run_model(10)
    e = time.time()
    print(f'{e-b} seconds')


