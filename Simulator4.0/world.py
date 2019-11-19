import json
from datetime import datetime
import simpy
from schema import Schema, SchemaError

class SimulationWorld:
    """The world starts here. It sets the simulation world.
    The simulation world can be configured with the following characteristics:
    :param int sim_duration: duration of the simulation
    :param str blockchain: the type of blockchain being simulated (e.g. bitcoin or ethereum)
    :param dict time_between_block_distribution: Probability distribution to represent the time between blocks
    :param dict validate_block_distribution: Probability distribution to represent the block validation delay
    Each distribution is represented as dictionary, with the following schema:
    ``{ 'name': str, 'parameters': tuple }``
    We use SciPy to work with probability distributions.
    You can see a complete list of distributions here:
    https://docs.scipy.org/doc/scipy/reference/stats.html
    You can use the ``scripts/test-fit-distribution.py`` to find a good distribution 
        and its parameters which fits your input data measured.
    """

    def __init__(self,
                 sim_duration: int,
                 initial_time: int,
                 config_file: str,
                 measured_latency: str,
                 measured_throughput_received: str,
                 measured_throughput_sent: str,
                 measured_delays: str):
        self._sim_duration = sim_duration
        self._initial_time = initial_time
        self._config = self._read_json_file(config_file)
        self._latency = self._read_json_file(measured_latency)
        self._throughput_received = self._read_json_file(measured_throughput_received)
        self._throughput_sent = self._read_json_file(measured_throughput_sent)
        self._delays = self._read_json_file(measured_delays)
        # Set the SimPy Environment
        self.env = simpy.Environment(initial_time=self._initial_time)
        self._set_configs()
        self._set_delays()
        self._set_latencies()
        self._set_throughputs()
        # Set the monitor
        end_simulation = self._initial_time + self._sim_duration
        self.env.data = {        
            'block_propagation': {},  
        }

    def blockchain(self):
        return self.env.config['blockchain']

    def locations(self):
        return self._locations

    def start_simulation(self):
        end = self._initial_time + self._sim_duration
        self.env.run(until=end)

    def _set_configs(self):
        """Injects the different configuration variables to the environment variable to be
        used during the simulation"""
        self.env.config = self._config

    def _set_delays(self):
        """Injects the probability distribution delays in the environment variable to be
        used during the simulation"""
        blockchain_switcher = {
            'bitcoin': self._set_bitcoin_delays(),
            'ethereum': self._set_ethereum_delays()
        }
        return blockchain_switcher.get(self.blockchain, lambda: "Invalid blockchain")()

    def _set_bitcoin_delays(self):
        self._validate_distribution(
            # self._delays['bitcoin']['tx_validation'],
            self._delays['bitcoin']['block_validation'],
            self._delays['bitcoin']['time_between_blocks_seconds'])
        self.env.delays = self._delays['bitcoin']

    def _set_ethereum_delays(self):
        self._validate_distribution(
            # self._measured_delays['ethereum']['tx_validation'],
            self._delays['ethereum']['block_validation'],
            self._delays['ethereum']['time_between_blocks_seconds'])
        self.env.delays = self._delays['ethereum']

    def _set_latencies(self):
        """Reads the file with the latencies measurements taken"""
        self._locations = list(self._latency['locations'])
        self.env.delays.update(dict(LATENCIES=self._latency['locations']))

    def _set_throughputs(self):
        """Reads the measured throughputs and pass it to the environment variable to be
        used during the simulation"""
    
        # Check if all locations exist
        locations_rcvd = list(self._throughput_received['locations'])
        locations_sent = list(self._throughput_sent['locations'])
        if locations_rcvd != self.locations() or locations_sent != self.locations():
            raise RuntimeError(
                "The locations in latencies measurements are not equal in throughputs measurements")
        # Pass the throughputs to the environment variable
        self.env.delays.update(dict(
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
