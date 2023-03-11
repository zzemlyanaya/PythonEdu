import socket
import ssl
import base64

server = 'smtp.mail.ru'
port = 465
email = 'ee-tester@mail.ru'
pswd = 'TV23rL8gmZWQACeGTuPY'


def create_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    ssl_sock = ssl.wrap_socket(sock)
    hello = ssl_sock.recv(1024)
    print('S: ' + hello.decode())
    return ssl_sock


def send(sock, request, isCommand=True):
    sock.send(bytes(request + '\r\n', 'utf-8'))
    print('C: ' + request)
    if (isCommand):
        response = sock.recv(1024)
        print('S: ' + response.decode())


def b64e(input):
    input_bytes = input.encode()
    encoded_bytes = base64.b64encode(input_bytes)
    return encoded_bytes.decode();


sock = create_sock()
send(sock, 'EHLO anon')
send(sock, 'AUTH LOGIN')
send(sock, b64e(email))
send(sock, b64e(pswd))
send(sock, 'MAIL FROM: ' + email)
send(sock, 'RCPT TO: ' + email)
send(sock, 'DATA')

send(sock, 'From: ' + email, False)
send(sock, 'To: ' + email, False)
send(sock, 'Subject: TOP SECRET', False)
send(sock, '', False)
send(sock, 'Heeelo, my friend!', False)
send(sock, 'Heeelo, my friend!(2)', False)
send(sock, '..', False)
send(sock, 'Heeelo, my friend!(3)', False)
send(sock, '.')
send(sock, 'QUIT')


