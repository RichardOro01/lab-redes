"""Proxy web server"""
from socket import socket, AF_INET, SOCK_STREAM
import sys
import re
import os

PORT = 8888
WEB_SERVER_PORT = 80


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


def create_directory_if_not_exists(directory):
    """
    Create a directory if it does not already exist.

    Args:
        directory (str): The directory path to be created.

    Returns:
        None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


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


def start_server(tcp_server_socket):
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
            print(f'Received a connection from: {addr[0]}:{addr[1]}')
            message = tcp_client_socket.recv(1024)
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
                    tcp_client_socket.sendall(response.encode())
                    print('Read from cache')
            except IOError:
                if not file_exist:
                    web_socket = socket(AF_INET, SOCK_STREAM)
                    print(f"Connecting to {hostn}:{WEB_SERVER_PORT}")
                    try:
                        web_socket.connect((hostn, WEB_SERVER_PORT))
                        web_socket.sendall(
                            f"GET http://{filename} HTTP/1.0\n\n".encode())
                        while True:
                            buffer = web_socket.recv(1024)
                            if len(buffer) == 0:
                                break
                            create_directory_if_not_exists(f"cache/{hostn}")
                            with open(f"cache/{hostn}/{filename}", "wb") as tmp_file:
                                tmp_file.write(buffer)
                            tcp_client_socket.sendall(buffer)
                    except Exception as error:
                        print("Illegal request")
                        print(error)
                else:
                    response = "HTTP/1.0 404 Not Found\r\nContent-Type:text/html\r\n\r\n\r\n404 Not Found"
                    tcp_client_socket.sendall(response.encode())
            tcp_client_socket.close()
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
