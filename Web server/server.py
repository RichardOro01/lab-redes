"""Web server."""
from socket import socket, AF_INET, SOCK_STREAM
import threading
import time
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)
PORT = 8080
SRC = 'page'
serverSocket.bind(("127.0.0.1", PORT))
serverSocket.listen(1)


def is_socket_alive(sock):
    """Check if socket connection is alive"""
    try:
        sock.send(b'')
        return True
    except Exception:
        return False


def send_response(filename, connection_socket, e404=False):
    """Send html respond. Throw 404 in not found case"""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            output_data = file.read(1024)
            file.close()
            connection_socket.send(
                f'HTTP/1.1 {"404 Not Found" if e404 else ""} \r\n\r\n'.encode())
            connection_socket.sendall(output_data.encode())
    except IOError:
        if not e404:
            if is_socket_alive(connection_socket):
                send_response(f"{SRC}/404.html", connection_socket, True)
        else:
            print(
                "No such file 404.html, ensure you are running on root web server directory")
            if is_socket_alive(connection_socket):
                connection_socket.send(
                    'HTTP/1.1 404 Not Found \r\n\r\n'.encode())
        connection_socket.close()


def handle_client(connection_socket, address):
    """Handle client in a new thread"""
    print(f"Client connected from: {address[0]}:{address[1]}")
    time.sleep(3)
    message = connection_socket.recv(1024).decode()
    message = message.split()
    if len(message) >= 1:
        filename = message[1]
        if filename == '/':
            filename = f"{SRC}/index.html"
        else:
            filename = f"{SRC}{filename}.html"
        send_response(filename, connection_socket)
    connection_socket.close()
    print(f"Connection finished from: {address[0]}:{address[1]}")


def start_server():
    """Start server to listen"""
    connection_socket = None
    try:
        while True:
            print('Ready to serve...')
            connection_socket, address = serverSocket.accept()
            client_handler = threading.Thread(target=handle_client,
                                              args=(connection_socket, address))
            client_handler.start()
    except KeyboardInterrupt:
        if connection_socket and is_socket_alive(connection_socket):
            connection_socket.close()
        serverSocket.close()
        print("\nClosed server!")
        sys.exit(1)


if __name__ == "__main__":
    start_server()
