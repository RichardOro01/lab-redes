from socket import socket, AF_INET, SOCK_STREAM
import sys


def configureWebServer():
    serverName = input('Write server host: ')
    serverPort = int(input('Write server port: '))
    makeRequest(serverName, serverPort)


def makeRequest(serverName, serverPort):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    sentence = input('Input lowercase sentence: ')
    print(f'Sending request to {serverName}:{serverPort}')
    clientSocket.send(f'GET /{sentence} HTTP/1.1'.encode())
    print(f'Waiting for response from {serverName}:{serverPort}')
    modifiedSentence = clientSocket.recv(1024)
    print('From Server: ', modifiedSentence.decode())
    clientSocket.close()
    another = input('Another request? (y,n): ')
    if another == 'y':
        makeRequest(serverName, serverPort)
    else:
        sys.exit()


if __name__ == '__main__':
    configureWebServer()
