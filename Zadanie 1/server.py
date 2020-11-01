import http.server as http
from generator import generate_coordinates
import requests


def run(server_class=http.HTTPServer, handler_class=http.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()


