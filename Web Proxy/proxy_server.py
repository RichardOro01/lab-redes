"""Proxy web server"""
from socket import socket, AF_INET, SOCK_STREAM
import sys
import re
import os
import threading
import ssl

PORT = 8888
WEB_SERVER_DEFAULT_PORT = 80


def verify_params():
    """
    Verify the parameters passed to the script and exit if they are invalid.

    This function checks if the number of command-line arguments is less than or equal to 1. 
    If it is, it prints a usage message indicating how to run the script correctly and exits with a status code of 2.

    Parameters:
        None

    Returns:
        None
    """
    if len(sys.argv) <= 1:
        print(
            'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
        sys.exit(2)


def create_directory_if_not_exists(directory: str):
    """
    Create a directory if it does not already exist.

    Args:
        directory (str): The directory path to be created.

    Returns:
        None
    """
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory)


def validate_ip(ip: str):
    """
    Validates an IP address.

    Args:
        ip (str): The IP address to be validated.

    Returns:
        bool: True if the IP address is valid, False otherwise.
    """
    ip_regexp = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(ip_regexp, ip) or ip == "localhost"


def verify_ip():
    """
    Verify the given IP address.

    Args:
        None

    Returns:
        None
    """
    if not validate_ip(sys.argv[1]):
        print("Invalid ip")
        sys.exit(2)


def init_socket():
    """
    Initializes a socket and binds it to the specified address and PORT.

    Returns:
        The initialized TCP server socket.

    Raises:
        OSError: If there is an error binding the socket.
    """
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    try:
        tcp_server_socket.bind((sys.argv[1], PORT))
        tcp_server_socket.listen()
        return tcp_server_socket
    except OSError as error:
        print(error)
        sys.exit(2)


def destructure_url(url: str):
    temp = url
    http_pos = url.find("://")
    if http_pos == -1:
        temp = url
    else:
        temp = url[(http_pos+3):]
    web_server_pos = temp.find("/")
    file_name = ""
    if web_server_pos == -1:
        web_server_pos = len(temp)
    else:
        file_name = temp[web_server_pos:]
    port_pos = temp.find(":")
    web_server = ""
    port = -1
    if (port_pos == -1 or web_server_pos < port_pos):
        port = WEB_SERVER_DEFAULT_PORT
        web_server = temp[:web_server_pos]

    else:
        port = int((temp[(port_pos+1):])[:web_server_pos-port_pos-1])
        web_server = temp[:port_pos]
    return (web_server, port, file_name)


def handle_get(tcp_client_socket: socket, split_message: list):
    split_message[1] = split_message[1].strip("/")
    url: str = split_message[1]
    message = " ".join(split_message)
    print("Web Request: ", url)
    url_destructured = destructure_url(url)
    hostn = url_destructured[0]
    hostp = url_destructured[1]
    file_name = url_destructured[2]
    print("Host name: ", hostn)
    print("Port: ", hostp)
    print("File name: ", file_name)
    file_exist = False
    route = f"{hostn}/index"
    if file_name == "":
        file_name = "/"
    if file_name[1:] != "":
        route = f"{hostn}/{file_name}"
    try:
        with open(f"cache/{route}", "r", encoding="utf-8") as file:
            output_data = file.readlines()
            file_exist = True
            response = "HTTP/1.0 200 OK\r\nContent-Type:text/html\r\n"
            response += "\r\n".join(output_data)
            tcp_client_socket.sendall(response.encode())
            print('Read from cache')
    except IOError:
        if not file_exist:
            web_socket = socket(AF_INET, SOCK_STREAM)
            print(f"Connecting to {hostn}:{hostp}")
            try:
                web_socket.connect((hostn, hostp))
                print("Sending request to web server:")
                print(message.encode())
                web_socket.sendall(
                    f"GET {file_name} HTTP/1.1\r\nHost: {hostn}:{hostp}\r\n\r\n".encode())
                print("Receiving response from web server and sending to client")
                create_directory_if_not_exists(
                    f"cache/{hostn}")
                has_response = False
                with open(f"cache/{route}", "wb") as tmp_file:
                    while True:
                        buffer = web_socket.recv(1024)
                        if len(buffer) == 0:
                            tmp_file.close()
                            break
                        has_response = True
                        tmp_file.write(buffer)
                        tcp_client_socket.sendall(buffer)
                if has_response:
                    print("Response sended to client")
                else:
                    print("Response not sended to client")
            except Exception as error:
                print("Illegal request")
                print(error)
        else:
            response = "HTTP/1.0 404 Not Found\r\nContent-Type:text/html\r\n\r\n\r\n404 Not Found"
            tcp_client_socket.sendall(response.encode())


def handle_connect(tcp_client_socket: socket, split_message: list):
    context = ssl.create_default_context()
    host: str = split_message[1]
    host_partition = host.partition(":")
    hostn = host_partition[0]
    hostp = host_partition[2]
    has_ssl = False
    if hostp == "":
        hostp = WEB_SERVER_DEFAULT_PORT
    else:
        hostp = int(hostp)
    web_socket = socket(AF_INET, SOCK_STREAM)
    print(f"Connecting with {host}:")
    web_socket.connect((hostn, hostp))
    current_socket = web_socket
    if hostp == 443:
        print("Creating a SSL connection")
        current_socket = context.wrap_socket(web_socket, server_hostname=hostn)
        has_ssl = True
    message = " ".join(split_message)
    print("Sending request to web server:")
    print(message.encode())
    current_socket.sendall(message.encode())
    print("Receiving response from web server and sending to client")
    response = b""
    while True:
        buffer = current_socket.recv(1024)
        if len(buffer) == 0:
            break
        response += buffer
        tcp_client_socket.sendall(buffer)
    if response != b"":
        print("Response sended to client")
        print(response.decode())
    else:
        print("Response not sended to client")
    current_socket.close()
    if has_ssl:
        web_socket.close()


def handle_connection(tcp_client_socket: socket, addr: tuple):
    try:
        print(f'Received a connection from: {addr[0]}:{addr[1]}')
        message = tcp_client_socket.recv(1024)
        print("Request: ", message)
        message = message.decode()
        split_message = message.split(" ")
        print("Type: ", split_message[0])
        if split_message[0] == "GET":
            handle_get(tcp_client_socket, split_message)
        elif split_message[0] == "CONNECT":
            handle_connect(tcp_client_socket, split_message)
        tcp_client_socket.close()
    except Exception as error:
        print(error)


def start_server(tcp_server_socket: socket):
    """
    Function to start the server and handle incoming client requests.

    Parameters:
    - tcp_server_socket: The TCP server socket object.

    Returns: None
    """
    try:
        while True:
            print(f'Ready to serve on {sys.argv[1]}:{PORT}...')
            tcp_client_socket, addr = tcp_server_socket.accept()
            connection_handler = threading.Thread(target=handle_connection,
                                                  args=(tcp_client_socket, addr))
            connection_handler.daemon = True
            connection_handler.start()
    except InterruptedError:
        tcp_server_socket.close()
        print("Proxy closed")
        sys.exit(1)


def main():
    """
    Executes the main function of the program.

    This function is responsible for executing the main logic of the program. It performs the following steps:
    1. Verifies the parameters.
    2. Creates a directory named "cache" if it doesn't already exist.
    3. Verifies the IP address.
    4. Initializes a TCP server socket.
    5. Starts the server.

    Parameters:
        None

    Returns:
        None
    """
    verify_params()
    create_directory_if_not_exists("cache")
    verify_ip()
    tcp_server_socket = init_socket()
    start_server(tcp_server_socket)


if __name__ == "__main__":
    main()
