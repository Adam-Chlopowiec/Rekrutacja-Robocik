import socket
import json
import numpy as np


def calculate_speed(A, B, time):
    x1, y1, z1 = A[0], A[1], A[2]
    x2, y2, z2 = B[0], B[1], B[2]
    return np.sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2 + (z2 - z1) ^ 2) / time


def create_host(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def parse_response(response):
    response = response.decode('utf-8')
    headers, response_body = response.split('\n\n')
    protocol, headers = headers.splitlines()[0], headers.splitlines()[0:]
    headers = dict(headers)
    response_body = json.loads(response_body)
    return protocol, headers, response_body


def request_get(sock, host):
    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % host
    sock.send(request.encode())


def main(t=1):
    host = socket.gethostname()
    s = create_host(host, 8000)
    request_get(s, host)

    points = []
    speed = []
    while True:
        protocol, headers, response_body = parse_response(s.recv(1024))
        points += response_body
        if len(points) > 1:
            speed += calculate_speed(points[-1], points[-2], t)
        if headers['Connection'] == 'close':
            break

    print(points)
    print(speed)


if __name__ == '__main__':
    main()
