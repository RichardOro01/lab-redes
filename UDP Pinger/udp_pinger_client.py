"""UDPPingerClient.py"""
import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12000
PING_AMOUNT = 10
TIMEOUT = 1

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

packets_received = 0

for sequence_number in range(1, PING_AMOUNT+1):
    request_time = time.time()
    client_socket.sendto('hola'.encode("utf-8"), (SERVER_IP, SERVER_PORT))
    try:
        response, address = client_socket.recvfrom(1024)
    except socket.timeout:
        print(
            f"Ping: {sequence_number}: Se agotó el tiempo de espera de la solicitud")
        continue
    rtt = time.time() - request_time
    print(f"Ping {sequence_number}: RTT: {rtt} ms")
    packets_received = packets_received + 1

print(f'Packets sended: {PING_AMOUNT}')
print(f'Packets received: {packets_received}')
print(f'Packet loss: {(PING_AMOUNT-packets_received)/PING_AMOUNT*100}%')

client_socket.close()
