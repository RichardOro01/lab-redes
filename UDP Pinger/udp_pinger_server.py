"""UDPPingerServer.py"""
import random
from socket import socket, AF_INET, SOCK_DGRAM


PORT = 12000
HOST = 'localhost'

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))

while True:
    print('ready to ping')
    rand = random.randint(0, 10)
    message, address = serverSocket.recvfrom(1024)
    message = message.upper()
    if rand < 4:
        print('Packet lost')
        continue
    serverSocket.sendto(message, address)
    print(f"ping sended to {address[0]}:{address[1]}")
