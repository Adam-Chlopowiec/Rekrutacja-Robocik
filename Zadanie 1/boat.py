import socket
import json
import sys
from time import sleep
from numpy.random import random


def generate_coordinates():
    """
    Creates three random coordinates
    :return: Tuple with three random coordinates
    """
    return random(), random(), random()


class Boat:
    """
    Class Boat acts as simulation. Boat sends random coordinates to client with HTTP protocol "n" times with "time"
    interval
    """
    def __init__(self, n=3, time=1):
        """
        :param n: Specifies how many times boat sends coordinates (default = 3)
        :param time: Specifies time interval
        """
        self.boat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boat.bind((socket.gethostname(), 8000))
        self.n = n
        self.time = time

    def run(self) -> None:
        """
        Runs the simulation accepting connection from client and sending coordinates. Changes "Connection" header
        to close at the end.
        :return: None
        """
        self.boat.listen(5)
        client, addr = self.boat.accept()

        for i in range(self.n):
            response_body = json.dumps((generate_coordinates(), self.time))
            if i < self.n - 1:
                client.send(bytes("HTTP/1.1 200 OK\n"
                                  + "Content-Type: application/json\n"
                                  + "Content-Length: " + str(len(response_body)) + "\n"
                                  + "Connection: keep-alive" + "\n"
                                  + "\n"
                                  + response_body + '\n', "utf-8"))
            else:
                client.send(bytes("HTTP/1.1 200 OK\n"
                                  + "Content-Type: application/json\n"
                                  + "Content-Length: " + str(len(response_body)) + "\n"
                                  + "Connection: close" + "\n"
                                  + "\n"
                                  + response_body + '\n', "utf-8"))
            sleep(self.time)

        client.close()


if __name__ == "__main__":
    n = int(sys.argv[1])
    if n < 5:
        raise Exception("First argument can't be lower than 5")
    t = int(sys.argv[2])
    if t < 0:
        raise Exception("Second argument can't be lower than 0")
    Boat(n, t).run()
