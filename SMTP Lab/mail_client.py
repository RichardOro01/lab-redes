import base64
from socket import AF_INET, SOCK_STREAM, socket
import ssl

MSG = "\r\n I love computer networks!"
ENDMSG = "\r\n.\r\n"
FROM = "garciaj1246@gmail.com"
PASSWORD = "aosl duee njgo zqer"
RCPT = "hernandezl3003@gmail.com"

# Choose a mail server (e.g. Google mail server) and call it mailserver
MAILSERVER = 'smtp.gmail.com'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((MAILSERVER, 587))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

clientSocket.send("STARTTLS\r\n".encode())
tls_recv = clientSocket.recv(1024).decode()
print(tls_recv)

# SSL context
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=MAILSERVER)

# Authentication
username64 = base64.b64encode(FROM.encode()).decode()
password64 = base64.b64encode(PASSWORD.encode()).decode()

authMsg = "AUTH LOGIN\r\n".encode()
clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024)
print(recv_auth.decode())

authMsg = username64.encode()+"\r\n".encode()
clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024)
print(recv_auth.decode())

authMsg = password64.encode()+"\r\n".encode()
clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024)
print(recv_auth.decode())

# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: <"+FROM+">\r\n"
clientSocket.send(mailFrom.encode())
recv2 = clientSocket.recv(1024)
print(recv2)

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <"+RCPT+">\r\n"
clientSocket.send(rcptTo.encode())
recv3 = clientSocket.recv(1024)
print(recv3)

# Send DATA command and print server response.
data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024)
print(recv4)

# Send message data.
clientSocket.send(MSG.encode())

# Message ends with a single period.
clientSocket.send(ENDMSG.encode())
recv5 = clientSocket.recv(1024)
print(recv5)

# Send QUIT command and get server response.
quitCommand = "QUIT\r\n"
clientSocket.send(quitCommand.encode())
recv6 = clientSocket.recv(1024)
print(recv6)

clientSocket.close()
