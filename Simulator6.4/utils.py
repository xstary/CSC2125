import binascii
from datetime import datetime
import random
from ast import literal_eval as make_tuple
import scipy.stats



def get_latency_delay(network, origin: str, destination: str, n=1):
    distribution = network.delays['LATENCIES'][origin][destination]
    # Convert latency in ms
    latencies = get_random_values(distribution, n)[0]
    while latencies <= 0:
        latencies = get_random_values(distribution, n)[0]
    return latencies



def get_received_delay(network, message_size: float, origin: str, destination: str, n=1):
    """
    It calculates the delay when rdownloading a message with message_size
    """
    distribution = network.delays['THROUGHPUT_RECEIVED'][destination]
    delay = _calc_throughput(distribution, message_size, n)
    return delay


def get_upload_delay(network, message_size: float, origin: str, destination: str, n=1):
    """
    It calculates the delay when uploading a message with message_size
    """
    distribution = network.delays['THROUGHPUT_SENT'][origin]
    delay = _calc_throughput(distribution, message_size, n)
    return delay

def get_BP_delay(network, message_size, origin, destination):
    #return delay in milliseconds
    upl = get_upload_delay(network, message_size, origin, destination, n=1)
    dol = get_received_delay(network, message_size, origin, destination, n=1)
    delay = get_latency_delay(network, origin, destination, n=1) +\
            max(upl,dol)
    return delay 


def _calc_throughput(distribution: dict, message_size: float, n):
    throughput = get_random_values(distribution, n)[0]
    throughput = kB_to_MB(throughput)
    delay = (message_size * 8) / throughput
    while delay <= 0 :
        throughput = get_random_values(distribution, 1)[0]
        delay = (message_size * 8) / throughput
    return delay*1000


def time(simulator):
    return datetime.utcfromtimestamp(simulator.now).strftime('%m-%d %H:%M:%S')


def kB_to_MB(value):
    return value / 1000


def get_random_values(distribution: dict, n=1):
    """Receives a distribution and outputs n random values
    Distribution format: { \'name\': str, \'parameters\': tuple }"""
    dist = getattr(scipy.stats, distribution['name']) 
    if distribution['name'] != "pareto":
        param = make_tuple(distribution['parameters'])
        return dist.rvs(*param[:-2], loc=param[-2], scale=param[-1], size=n)
    else:
        param = distribution['parameters']*0.8
        return dist.rvs(b=5, scale=param, size=n)



