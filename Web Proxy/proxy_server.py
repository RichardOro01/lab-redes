"""Proxy web server"""
from socket import socket, AF_INET, SOCK_STREAM
import sys
import re
import os

PORT = 8888

if len(sys.argv) <= 1:
    print(
        'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

if not os.path.exists("cache"):
    os.makedirs("cache")


def validate_ip(ip):
    """
    Validates an IP address.

    Args:
        ip (str): The IP address to be validated.

    Returns:
        bool: True if the IP address is valid, False otherwise.
    """
    ip_regexp = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(ip_regexp, ip) or ip == "localhost"


if not validate_ip(sys.argv[1]):
    print("Invalid ip")
    sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
try:
    tcpSerSock.bind((sys.argv[1], PORT))
except OSError as error:
    print(error)
    sys.exit(2)

tcpSerSock.listen()
try:
    while True:
        print(f'Ready to serve on {sys.argv[1]}:{PORT}...')
        tcpCliSock, addr = tcpSerSock.accept()
        print(f'Received a connection from: {addr[0]}:{addr[1]}')
        message = tcpCliSock.recv(1024)
        print("Request: ", message)
        message = message.decode()
        web_request = message.split()[1]
        web_request = web_request.strip("/")
        print("Web Request: ", web_request)
        request_partition = web_request.partition("/")
        filename = request_partition[2]
        hostn = request_partition[0]
        print("File name: ", filename)
        file_exist = False
        file_to_use = "/" + filename
        print("File to use: ", file_to_use)
        try:
            with open(f"cache/{hostn}/{file_to_use[1:]}", "r", encoding="utf-8") as file:
                output_data = file.readlines()
                file_exist = True
                response = "HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n"
                response += "\r\n".join(output_data)
                tcpCliSock.sendall(response.encode())
                print('Read from cache')
        except IOError:
            if not file_exist:
                web_socket = socket(AF_INET, SOCK_STREAM)
                WEB_SERVER_PORT = 80
                print(f"Connecting to {hostn}:{WEB_SERVER_PORT}")
                try:
                    web_socket.connect((hostn, WEB_SERVER_PORT))
                    web_socket.sendall(
                        f"GET http://{filename} HTTP/1.0\n\n".encode())
                    while True:
                        buffer = web_socket.recv(1024)
                        if len(buffer) == 0:
                            break
                        if not os.path.exists(f"cache/{hostn}"):
                            os.makedirs(f"cache/{hostn}")
                        with open(f"cache/{hostn}/{filename}", "wb") as tmpFile:
                            tmpFile.write(buffer)
                        tcpCliSock.sendall(buffer)
                except Exception as error:
                    print("Illegal request")
                    print(error)
            else:
                response = "HTTP/1.0 404 Not Found\r\nContent-Type:text/html\r\n\r\n\r\n404 Not Found"
                tcpCliSock.sendall(response.encode())
        tcpCliSock.close()
except InterruptedError:
    tcpSerSock.close()
    print("Proxy closed")
    sys.exit(1)
