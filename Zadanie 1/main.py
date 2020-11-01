import http.server as http
from generator import generate_coordinates
import requests


def send_coords():
    coords = generate_coordinates()
    requests.post('http://localhost:8000', coords.__str__())


def get_coords():
    response = requests.get('http://localhost:8000')
    print(response.text)


if __name__ == '__main__':
    send_coords()
    get_coords()
