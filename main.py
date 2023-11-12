"""Web server."""
from socket import socket, AF_INET, SOCK_STREAM

serverSocket = socket(AF_INET, SOCK_STREAM)
PORT = 80
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
            for _, data in enumerate(output_data):
                connection_socket.send(data.encode())
            connection_socket.send("\r\n".encode())
    except IOError:
        if is_socket_alive(connection_socket):
            send_response(f"{SRC}/404.html", connection_socket, True)
        connection_socket.close()


def server():
    """Start server to listen"""
    try:
        while True:
            print('Ready to serve...')
            connection_socket, _ = serverSocket.accept()
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
    except KeyboardInterrupt:
        connection_socket.close()
        print("\nServidor cerrado!")


server()
