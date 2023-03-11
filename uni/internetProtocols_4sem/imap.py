import socket
import ssl
import base64

server = 'imap.mail.ru'
port = 993
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
        response = sock.recv(100500)
        print('S: ' + response.decode())


def b64e(input):
    input_bytes = input.encode()
    encoded_bytes = base64.b64encode(input_bytes)
    return encoded_bytes.decode();


sock = create_sock()

send(sock, 'CMD1 LOGIN ' + email + ' ' + pswd)
send(sock, 'CMD2 SELECT Inbox')  # Выбор папки входящих сообщений
send(sock, 'CMD3 SEARCH')  # Получение идетификаторов всех сообщений
send(sock, 'CMD4 SEARCH FLAGGED')  # Получение идетификаторов важных сообщений
send(sock, 'CMD5 SEARCH 1:20')  # Получение первых 20-ти сообщений

send(sock, 'CMD6 FETCH 1 UID')  # получене глобального идентификатора первого сообщения
# send(sock, 'CMD7 FETCH 1 BODY[HEADER]') #получене всех заголовков
# send(sock, 'CMD8 FETCH 1 (BODY[HEADER.FIELDS (Date From To Subject)])') #получене определённых заголовков
# send(sock, 'CMD9 FETCH 6 FLAGS') #получене флагов
# send(sock, 'CMD10 FETCH 6 (FLAGS BODY[HEADER.FIELDS (Date From Subject To)] BODY[TEXT])') #получене смешанных полей
# send(sock, 'CMD11 FETCH 6 BODYSTRUCTURE') #получене информации о структуре сообщения (наменование, размеры и форматы сообщений (парсим регвырами))




