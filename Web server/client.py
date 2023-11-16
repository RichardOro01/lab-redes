"""Web client."""
from socket import socket, AF_INET, SOCK_STREAM
import sys


def configure_web_server():
    """Configure host and post."""
    server_name = input('Write server host: ')
    server_port = int(input('Write server port: '))
    input_request_file(server_name, server_port)


def input_request_file(server_name, server_port):
    """Input request file."""
    file = input('Input lowercase sentence: ')
    make_request(server_name, server_port, file)
    another = input('Another request? (y,n): ')
    if another == 'y':
        input_request_file(server_name, server_port)
    else:
        sys.exit()


def make_request(server_name, server_port, file):
    """Make a request to a file."""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    print(f'Sending request to {server_name}:{server_port}')
    client_socket.send(f'GET /{file} HTTP/1.1'.encode())
    print(f'Waiting for response from {server_name}:{server_port}')
    response = client_socket.recv(2048)
    print('From Server: ', response.decode())
    client_socket.close()


if __name__ == '__main__':
    configure_web_server()
