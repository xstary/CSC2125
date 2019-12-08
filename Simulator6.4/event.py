from utils import *
import random
import numpy as np
import scipy

class Event:
    def __init__(self, ty, node, time, msg=None):  
        self.type = ty # Block Propogation (BP) or Block Mining (BM)
        self.node = node
        self.time = time
        self.msg = msg # only used for BP messages

