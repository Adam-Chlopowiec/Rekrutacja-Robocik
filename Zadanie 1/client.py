import socket
import json
import numpy as np


def calculate_speed(A, B, time):
    x1, y1, z1 = A[0], A[1], A[2]
    x2, y2, z2 = B[0], B[1], B[2]
    return np.sqrt((x2 - x1) ^ 2 + (y2 - y1) ^ 2 + (z2 - z1) ^ 2) / time


def main():
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, 8000))

    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % hostname
    s.send(request.encode())
    points = []
    speed = []
    while True:
        response = s.recv(4096).decode('utf-8')
        headers, response_body = response.split('\n\n')
        headers = dict(headers)
        t = response_body[3]
        response_body = json.loads(response_body[:3])
        points += response_body
        if len(points) > 1:
            speed += calculate_speed(points[-1], points[-2], t)

        if headers['Connection'] == 'close':
            break
    print(points)
    print(speed)


if __name__ == '__main__':
    main()
