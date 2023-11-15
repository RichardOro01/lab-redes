# UDPPingerClient.py
import socket
import time

# Ip y puerto del servidor
server_ip = "127.0.0.1"
server_port = 12000

# Tiempo de espera para la respuesta del servidor
timeout = 1

# Inicializar el socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enviar 10 mensajes ping al servidor
for sequence_number in range(1, 11):
    # Generar el mensaje ping
    message = "Ping {} {}".format(sequence_number, time.time())

    # Enviar el mensaje ping al servidor
    client_socket.sendto(message.encode("utf-8"), (server_ip, server_port))

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
    print("RTT: {} segundos".format(rtt))

# Cerrar el socket UDP
client_socket.close()
