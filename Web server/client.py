"""Web client."""
from socket import socket, AF_INET, SOCK_STREAM
import sys


def configure_web_server():
    """Configure host and post."""
    server_name = input('Write server host: ')
    server_port = int(input('Write server port: '))
    make_request(server_name, server_port)


def make_request(server_name, server_port):
    """Make a request to a file."""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    sentence = input('Input lowercase sentence: ')
    print(f'Sending request to {server_name}:{server_port}')
    client_socket.send(f'GET /{sentence} HTTP/1.1'.encode())
    print(f'Waiting for response from {server_name}:{server_port}')
    response = client_socket.recv(2048)
    print('From Server: ', response.decode())
    client_socket.close()
    another = input('Another request? (y,n): ')
    if another == 'y':
        make_request(server_name, server_port)
    else:
        sys.exit()


if __name__ == '__main__':
    configure_web_server()
