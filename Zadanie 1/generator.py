import numpy as np
from point import Point


def generate_coordinates():
    return np.random.random(), np.random.random(), np.random.random()


class Generator:
    def __init__(self, n, t):
        self.n = n
        self.t = t
