import socket
import json
from generator import generate_coordinates
from time import sleep


class Server:
    def __init__(self, n=3, t=1):
        self.boat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.boat.bind((socket.gethostname(), 8000))
        self.n = n
        self.t = t

    def run(self):
        self.boat.listen(5)
        client, addr = self.boat.accept()

        for i in range(self.n):
            response_body = json.dumps(generate_coordinates())
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
            sleep(self.t)

        client.close()


Server(3, 1).run()
