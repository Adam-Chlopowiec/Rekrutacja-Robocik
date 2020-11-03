import socket
import json
from numpy import sqrt


def calculate_speed(A: tuple, B: tuple, time: int) -> float:
    """
    Returns speed based on distance between points A and B and returns speed
    :param A: First point
    :param B: Second point
    :param time: Time between sending points A and B
    :return: Speed as floating point number
    """
    x1, y1, z1 = A[0], A[1], A[2]
    x2, y2, z2 = B[0], B[1], B[2]
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) / time


def create_host(host: str, port: int) -> socket.socket:
    """
    Returns socket connected to host at given port
    :param host: Host which socket will connect to
    :param port: Port at which socket will connect to host
    :return: Socket connected to host via IPv4 and TCP protocol
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def parse_response(response: bytes) -> tuple:
    """
    Parses response splitting given bytes into protocol, headers, content and time
    :param response: Response received in http protocol format
    :return: Protocol, headers, content and time
    """
    response = response.decode('utf-8')
    headers, content = response.split('\n\n')
    headers = headers.splitlines()
    protocol, headers = headers[0], headers[1:]
    keys, values = [], []
    for line in headers:
        line = line.split(": ")
        keys.append(line[0])
        values.append(line[1])

    headers = dict(zip(keys, values))
    content = json.loads(content)
    time = content[1]
    return protocol, headers, content[0], time


def request_get(sock: socket.socket, host: str) -> None:
    """
    Sends HTTP GET request to host
    :param sock: Socket sending request
    :param host: Host at which request will be sent
    :return: None
    """
    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % host
    sock.send(request.encode())


def main():
    host = socket.gethostname()
    s = create_host(host, 8000)
    request_get(s, host)

    points = []
    speed = []
    while True:
        protocol, headers, response_body, time = parse_response(s.recv(1024))
        points.append(response_body)
        if len(points) > 1:
            speed.append(calculate_speed(points[-1], points[-2], time))
            print(speed[-1])
        if headers['Connection'] == 'close':
            break


if __name__ == '__main__':
    main()
