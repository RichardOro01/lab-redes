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
    request = f"GET /{file} HTTP/1.1\r\nHost: {server_name}:{server_port}\r\n\r\n"
    client_socket.sendall(request.encode())
    print(f'Waiting for response from {server_name}:{server_port}')
    response = b""
    while True:
        packet_response = client_socket.recv(2048)
        if len(packet_response) == 0:
            break
        response += packet_response
    print('From Server: ', response.decode())
    client_socket.close()


if __name__ == '__main__':
    configure_web_server()
