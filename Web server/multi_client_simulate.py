from client import make_request
import threading

CLIENTS_AMOUNT = 10


def configure_web_server():
    """Configure host and post."""
    server_name = input('Write server host: ')
    server_port = int(input('Write server port: '))
    file = input('Write request file: ')
    for _ in range(CLIENTS_AMOUNT):
        client_thread = threading.Thread(
            target=make_request, args=(server_name, server_port, file))
        client_thread.start()


if __name__ == '__main__':
    configure_web_server()
