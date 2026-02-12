import numpy as np 
import random
import os
USE_NSLKDD = os.getenv('USE_NSLKDD', 'true').lower() == 'true'


def generate_sample(anomaly=False):
    use_nskldd =True
    if use_nskldd:
        if anomaly:
            return np.random.normal(3, 1.5, (1, 39)).astype(np.float32)
        return np.random.normal(0, 1, (1, 39)).astype(np.float32)
    else: 
        if anomaly: 
            return np.random.normal(8, 2, (1, 4))
        return np.random.normal(0, 1, (1, 4))
