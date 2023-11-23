"""Proxy web server"""
from socket import socket, AF_INET, SOCK_STREAM
import sys
import re

PORT = 8888

if len(sys.argv) <= 1:
    print(
        'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)


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
while True:
    print(f'Ready to serve on {sys.argv[1]}:{PORT}...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024)
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    file_exist = False
    file_to_use = "/" + filename
    print(file_to_use)
    try:
        with open(file_to_use[1:], "r", encoding="utf-8") as file:
            output_data = file.readlines()
            file_exist = True
            response = "HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n"
            response += "\r\n".join(output_data)
            tcpCliSock.sendall(response.encode())
            print('Read from cache')
    except IOError:
        if not file_exist:
            web_socket = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print(hostn)
            try:
                socket.connect((hostn, 80))
                fileobj = web_socket.makefile('r', 0)
                fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")
                buffer = fileobj.readlines()
                with open("./" + filename, "wb") as tmpFile:
                    tmpFile.write("\r\n".join(buffer))
                tcpCliSock.sendall("\r\n".join(buffer).encode())
            except:
                print("Illegal request")
        else:
            response = "HTTP/1.0 404 Not Found\r\nContent-Type:text/html\r\n\r\n\r\n404 Not Found"
            tcpCliSock.sendall(response.encode())

    tcpSerSock.close()
    tcpCliSock.close()
