import binascii
from datetime import datetime
import random
from ast import literal_eval as make_tuple
import scipy.stats



def get_latency_delay(network, origin: str, destination: str, n=1):
    distribution = network.delays['LATENCIES'][origin][destination]
    # Convert latency in ms
    latencies = get_random_values(distribution, n)
    if len(latencies) == 1:
        if latencies[0] < 0:
            return 0
        return round(latencies[0], 4)
    else:
        return latencies


def get_received_delay(network, message_size: float, origin: str, destination: str, n=1):
    """
    It calculates and returns a delay when receiving/downloading a message with a certain size (`message_size`)
    :param message_size: message size in megabytes (MB)
    :param origin: the location of the origin node
    :param destination: the location of the destination node
    :param n: the number of delays returned
    If `n` is 1 it returns a `float`, if `n > 1` returns an array of `n` floats.
    """
    distribution = network.delays['THROUGHPUT_RECEIVED'][destination]
    delay = _calc_throughput(distribution, message_size, n)
    if delay < 0:
        return 0
    else:
        return delay


def get_upload_delay(network, message_size: float, origin: str, destination: str, n=1):
    """
    It calculates and returns a delay when sending/uploading a message with a certain size (`message_size`)
    :param message_size: message size in megabytes (MB)
    :param origin: the location of the origin node
    :param destination: the location of the destination node
    :param n: the number of delays returned
    If `n` is 1 it returns a `float`, if `n > 1` returns an array of `n` floats.
    """
    distribution = network.delays['THROUGHPUT_SENT'][origin]
    delay = _calc_throughput(distribution, message_size, n)
    if delay < 0:
        return 0
    else:
        return delay

def get_BP_delay(network, message_size, origin, destination):
    delay = get_upload_delay(network, message_size, origin, destination, n=1)
    delay += get_received_delay(network, message_size, origin, destination, n=1)
    delay += get_latency_delay(network, origin, destination, n=1)
    return delay #return time in milliseconds


def _calc_throughput(distribution: dict, message_size: float, n):
    rand_throughputs = get_random_values(distribution, n)
    delays = []
    # print(message_size)
    # print(rand_throughputs)
    for throughput in rand_throughputs:
        delay = (message_size * 8) / throughput
        delays.append(delay)
    # print(delays)
    if len(delays) == 1:
        return round(delays[0], 4)
    else:
        return delays


def time(simulator):
    return datetime.utcfromtimestamp(simulator.now).strftime('%m-%d %H:%M:%S')


def kB_to_MB(value):
    return value / 1000


def get_random_values(distribution: dict, n=1):
    """Receives a `distribution` and outputs `n` random values
    Distribution format: { \'name\': str, \'parameters\': tuple }"""
    dist = getattr(scipy.stats, distribution['name'])
    param = make_tuple(distribution['parameters'])
    return dist.rvs(*param[:-2], loc=param[-2], scale=param[-1], size=n)


# def decode_hex(s):
#     if isinstance(s, str):
#         return bytes.fromhex(s)
#     if isinstance(s, (bytes, bytearray)):
#         return binascii.unhexlify(s)
#     raise TypeError('Value must be an instance of str or bytes')


# def encode_hex(b):
#     if isinstance(b, str):
#         b = bytes(b, 'utf-8')
#     if isinstance(b, (bytes, bytearray)):
#         return str(binascii.hexlify(b), 'utf-8')
#     raise TypeError('Value must be an instance of str or bytes')


# def is_numeric(x):
#     return isinstance(x, int)


# def encode_int32(v):
#     return v.to_bytes(32, byteorder='big')
