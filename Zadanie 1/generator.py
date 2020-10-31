import numpy as np
from point import Point
from time import sleep

class Generator:
    def __init__(self, n, t):
        self.n = n
        self.t = t

    def generate_coordinates(self, t):
        for i in range(self.n):
            point = Point(np.random.random(), np.random.random(), np.random.random())
            sleep(t)