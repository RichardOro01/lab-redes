"""UDPPingerClient.py"""
import socket
import time

# Ip y puerto del servidor
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12000
PING_AMOUNT = 10

# Tiempo de espera para la respuesta del servidor
TIMEOUT = 1

# Inicializar el socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

# Enviar 10 mensajes ping al servidor
for sequence_number in range(1, PING_AMOUNT+1):
    # Generar el mensaje ping
    message = f"Ping {sequence_number} {time.time()}"

    # Enviar el mensaje ping al servidor
    client_socket.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))

    try:
        # Recibir la respuesta del servidor
        response, address = client_socket.recvfrom(1024)
    except socket.timeout:
        print("Se agotó el tiempo de espera de la solicitud")
        continue

    # Calcular el tiempo de ida y vuelta (RTT)
    rtt = time.time() - float(response.decode("utf-8").split(" ")[1])

    # Imprimir el mensaje de respuesta
    print(response.decode("utf-8"))

    # Imprimir el tiempo de ida y vuelta (RTT)
    print(f"RTT: {rtt} segundos")

# Cerrar el socket UDP
client_socket.close()
