import base64

import beautifultable
from beautifultable import BeautifulTable
from imap.utils import IMAPException
from imap.mail_parser import IMAParser
# from utils import IMAPException
# from mail_parser import IMAParser
from socket import AF_INET, SOCK_STREAM, gaierror, socket, timeout, error
from ssl import wrap_socket
from getpass import getpass


class HideousClient:
    def __init__(self, server_port: str, login: str, use_ssl: bool, all_mails: bool, mail_range: range):
        server_port = server_port.split(':')
        if len(server_port) != 2:
            raise ValueError('Incorrect address - must be in "server:port"')

        self.server = server_port[0]
        self.port = int(server_port[1])
        self.use_ssl = use_ssl
        self.all_mails = all_mails
        self.mail_range = mail_range
        self.counter = 1
        self.login = login
        self.password = getpass()
        self.parser = IMAParser()

    def receive(self, sock: socket):
        data = bytearray()
        try:
            while True:
                received_data = sock.recv(1024)
                data.extend(received_data)
                if b'*' not in received_data:
                    break
        except timeout:
            pass
        finally:
            data = data.decode('utf-8')
            print(data)
            return data

    @staticmethod
    def send(sock: socket, message: str):
        sock.send(message.encode('utf-8'))

    def setup_ssl(self, sock: socket):
        self.send(sock, f'A{self.counter} STARTTLS\r\n')
        self.receive(sock)
        self.counter += 1
        return wrap_socket(sock)

    def encode_user_and_password(self):
        byte_str = ('\x00' + self.login + '\x00' + self.password).encode()
        base64_str = base64.b64encode(byte_str).decode()
        return base64_str

    def run(self):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((self.server, self.port))
            sock.settimeout(5)

            try:
                self.receive(sock)
            except timeout:
                raise gaierror

            if self.use_ssl:
                sock = self.setup_ssl(sock)
                self.receive(sock)

            try:
                self.send(sock, f'A{self.counter} AUTHENTICATE PLAIN\r\n')
            except error:
                print('Can\'t connect without SSL')

            self.counter += 1
            self.receive(sock)

            self.send(sock, self.encode_user_and_password() + '\r\n')
            self.counter += 1
            login_response = self.receive(sock)
            if 'NO' in login_response:
                raise IMAPException(login_response[5:])

            self.send(sock, f'A{self.counter} SELECT INBOX\r\n')
            self.counter += 1
            response = self.receive(sock)
            overall = int(response.split('\n')[1].split(' ')[1])

            if overall == 0:
                print('No mails in the inbox')
                return

            mails = self.parser.get_messages_numbers(self.all_mails, overall, self.mail_range)
            if mails == -1:
                print('No mails with requested indexes found')
                return

            table = BeautifulTable()
            table.columns.header = ["ID", "FROM", "TO", "SUBJECT", "DATE", "SIZE", "ATTACHMENTS"]
            table.set_style(beautifultable.Style.STYLE_BOX)
            for number in mails:
                try:
                    sender, receiver, subject, date, size = self.parser.get_message_info(sock, int(number), self.counter)
                    self.counter += 2
                    attaches = self.parser.get_message_attachments(sock, int(number), self.counter)
                    self.counter += 1
                    data = [int(number), sender, receiver, subject, date, f'{size} bytes']
                    if attaches:
                        data.append(
                            f'ATTACHED {len(attaches)} FILES:\n' +\
                            '\n'.join(map(lambda x: f'{x[0] + 1}. {x[1][1]}: {x[1][0]} bytes', enumerate(attaches)))
                        )
                    else:
                        data.append('NO ATTACHMENTS')
                    if len(data) != 0:
                        table.rows.append(data)
                except IMAPException as e:
                    print(e)

            if len(table.rows) != 0:
                print('Found emails:')
                print(table)

            sock.send(f"A{self.counter} logout\r\n".encode())

