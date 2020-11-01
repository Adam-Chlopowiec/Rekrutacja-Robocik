import socket
import json
from generator import generate_coordinates
from time import sleep


def run():
    boat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    boat.bind((socket.gethostname(), 8000))
    boat.listen(5)
    client, addr = boat.accept()
    n, t = 5, 1

    for i in range(n):
        response_body = json.dumps((generate_coordinates(), t))
        if i < n - 1:
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
        sleep(t)

    client.close()
