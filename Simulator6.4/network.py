import json
from datetime import datetime
import simpy
from schema import Schema, SchemaError

class Network:
    def __init__(self,
                 name: str,
                 config_file: str,
                 measured_latency: str,
                 measured_throughput_received: str,
                 measured_throughput_sent: str,
                 measured_delays: str):

        self.config = self._read_json_file(config_file)
        self._latency = self._read_json_file(measured_latency)
        self._throughput_received = self._read_json_file(measured_throughput_received)
        self._throughput_sent = self._read_json_file(measured_throughput_sent)
        self._delays = self._read_json_file(measured_delays) 
        self._set_delays()
        self._set_latencies()
        self._set_throughputs()

        self.name = name
        self.blockchain = self.config['blockchain']
        self.number_of_connections = self.config[self.blockchain]['nconnections']
        self.difficulty = self.config[self.blockchain]['time_between_blocks_seconds'] #the target block generation time
        self.total_hashrate = 0
        self.nodes = {}
        self.miners = {}
        self.data = {}
        self.block_propagation = {}
        self.final_propagation_time = {}


    def blockchain(self):
        return self.config['blockchain']

    def locations(self):
        return self._locations


    def add_node(self, node):
        self.nodes[node.nid] = node
        self.total_hashrate += node.hashrate



    def _set_delays(self):
        if self.config['blockchain'] == "bitcoin": 
            self._set_bitcoin_delays(),
        elif self.config['blockchain'] == "ethereum": 
            self._set_ethereum_delays()
        else:
            print('Unknown Blockchain')

    def _set_bitcoin_delays(self):
        self._validate_distribution(
            self._delays['bitcoin']['block_validation'],
            self.config['bitcoin']['time_between_blocks_seconds'])
        self.delays = self._delays['bitcoin']

    def _set_ethereum_delays(self):
        self._validate_distribution(
            self._delays['ethereum']['block_validation'],
            self.config['ethereum']['time_between_blocks_seconds'])
        self.delays = self._delays['ethereum']

    def _set_latencies(self):
        """Reads the file with the latencies measurements"""
        self._locations = list(self._latency['locations'])
        self.delays.update(dict(LATENCIES=self._latency['locations']))

    def _set_throughputs(self):
        """Reads the measured throughputs to be
        used during the simulation"""
    
        # Check if all locations exist
        locations_rcvd = list(self._throughput_received['locations'])
        locations_sent = list(self._throughput_sent['locations'])
        if locations_rcvd != self.locations() or locations_sent != self.locations():
            raise RuntimeError(
                "The locations in latencies measurements are not equal in throughputs measurements")
        # Set the throughputs
        self.delays.update(dict(
            THROUGHPUT_RECEIVED=self._throughput_received['locations'],
            THROUGHPUT_SENT=self._throughput_sent['locations']
        ))

    def _validate_distribution(self, *distributions: dict):
        for distribution in distributions:
            distribution_schema = Schema({
                'name': str,
                'parameters': str
            })
            try:
                distribution_schema.validate(distribution)
            except SchemaError:
                raise TypeError(
                    'Probability distribution must follow this schema: { \'name\': str, \'parameters\': tuple as a string }')

    def _read_json_file(self, file_location):
        with open(file_location) as f:
            return json.load(f)
