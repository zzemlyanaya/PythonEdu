import base64
import os
import socket
import ssl
from ssl import SSLContext, CERT_REQUIRED
from getpass import getpass
from pathlib import Path

from smtp.mail_creator import HideousMailCreator
from smtp.utils import SMTPFile, SMTPAnswer, SMTPException


class HideousClient:
    def __init__(self,
                 addr_from: str, addr_to: str, subject: str, directory: str, server_port: str,
                 use_ssl: bool, need_auth: bool, print_log: bool):

        self.addr_from = addr_from
        self.addr_to = addr_to
        self.subject = subject
        self.use_ssl = use_ssl
        self.ssl_context = None
        self.need_auth = need_auth
        self.print_log = print_log
        self.dir = Path(directory).resolve()
        server_port = server_port.split(':')
        self.server = server_port[0]
        self.port = int(server_port[1])

        if self.need_auth:
            self.password = getpass()

        self.requests = []
        self.create_requests()

    def normalized_from(self):
        return self.addr_from.replace("@", ".")

    def create_requests(self):
        if self.need_auth:
            self.requests = [f'EHLO {self.normalized_from()}\n',
                             'auth login\n',
                             f'{base64.b64encode(self.addr_from.encode("utf-8")).decode("utf-8")}\n',
                             f'{base64.b64encode(self.password.encode("utf-8")).decode("utf-8")}\n',
                             f'MAIL FROM: <{self.addr_from}>\nRCPT TO: <{self.addr_to}>\nDATA\n']
        else:
            self.requests = [f'EHLO {self.normalized_from()}\n',
                             f'MAIL FROM: <{self.addr_from}>\nRCPT TO: <{self.addr_to}>\nDATA\n']

    def debug(self, text):
        if self.print_log:
            print(text)

    def create_mail(self):
        creator = HideousMailCreator()
        creator.add_header(self.addr_from, self.addr_to, self.subject)

        files = self.get_attachments()
        for i, file in enumerate(files):
            creator.add_attachment(file, is_last=i == len(files) - 1)

        return creator.get_mail()

    def get_attachments(self):
        res = []
        for file in os.listdir(self.dir):
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff', '.webp')):
                res.append(SMTPFile(Path(self.dir / file)))
        return res

    def setup_ssl(self, sock: socket):
        self.ssl_context = SSLContext()
        self.ssl_context.verify_mode = CERT_REQUIRED

        self.send(sock, f'EHLO {self.normalized_from()}\n')
        self.receive(sock)
        self.send(sock, 'starttls\n')
        self.receive(sock)
        return ssl.wrap_socket(sock)

    def receive(self, sock: socket):
        message = b''
        while True:
            try:
                string = sock.recv(1024)
                if string == b'':
                    break
                message += string

            except Exception:
                break

        message = message.decode('utf-8')
        self.debug(f'<----- SMTP Server: {message}')

        answer = SMTPAnswer.from_str(message)
        if answer.code > 499:
            raise Exception(answer.full_answer)

    def send(self, sock: socket, message: str):
        self.debug(f'SMTP Client ----->: {message}')
        sock.send(message.encode())

    def run(self):
        self.debug('Starting the mailing client')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            try:
                self.debug('Trying to connect to SMTP server.......')
                sock.connect((self.server, self.port))
                self.debug('Connected to SMTP server')

                if self.use_ssl:
                    self.debug('Trying to establish SSL.......')
                    sock = self.setup_ssl(sock)
                    self.debug('SSL established')

                for command in self.requests:
                    self.send(sock, command)
                    self.receive(sock)
                    if 'DATA' in command:
                        sock.send(self.create_mail().encode())
                        self.receive(sock)

            except SMTPException as e:
                print(e.msg)
