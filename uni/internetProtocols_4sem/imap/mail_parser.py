import re
import base64
import quopri
from socket import timeout
from typing import List

# from utils import IMAPException
from imap.utils import IMAPException


class IMAParser:
    def __init__(self):
        self.from_regex = re.compile(r'\nFrom: (.*?)\r\n\w'.encode(), flags=re.M | re.S)
        self.to_regex = re.compile(r'\nTo: (.*?)\r\n'.encode())
        self.subject_regex = re.compile(r'\nSubject:(.*?)\r\n\w'.encode(), flags=re.M | re.S)
        self.date_regex = re.compile(r'\nDate: (.*?)\r\n'.encode())
        self.size_regex = re.compile(r" \(RFC822.SIZE (.*)\)")
        self.attachment_regex = re.compile(r'(\d+) NIL \("attachment" \("filename" "(.*?)"\)', flags=re.M | re.S)

    @staticmethod
    def decode_header(data: bytes):
        data = data.decode()
        if '=?' not in data:
            return data
        data = data.split()
        res = ''
        for element in data:
            if '=?' in element:
                data_regex = re.compile(r'\?[bBqQ]\?(.*)\?=')
                st = data_regex.findall(element)[0]

                code_regex_b = re.compile(r"=\?(.*)\?[bB]")
                code_regex_q = re.compile(r"=\?(.*)\?[qQ]")

                # Quoted-printable aka MIME-HEADER
                if code_regex_q.match(element):
                    code = code_regex_q.findall(element)[0]
                    res += quopri.decodestring(st).decode(code)
                # Base64
                else:
                    code = code_regex_b.findall(element)[0]
                    res += base64.b64decode(st).decode(code)
            else:
                res += element
        return res

    def parse_headers(self, data):
        sender = self.from_regex.findall(data)[0]
        date = self.date_regex.findall(data)[0]
        receiver = self.to_regex.findall(data)[0]
        subject = self.subject_regex.findall(data)[0]
        return self.decode_header(sender), self.decode_header(receiver), \
               self.decode_header(subject), self.decode_header(date)

    def get_message_info(self, sock, number, counter):
        sock.send(f'A{counter} FETCH {number+1} BODY[HEADER]\r\n'.encode())
        headers = bytearray()
        try:
            while True:
                received_data = sock.recv(1024)
                headers.extend(received_data)
                if b'OK FETCH done\r\n' in received_data:
                    break
        except timeout:
            pass

        print(headers.decode())
        if not headers or b'(nothing matched)' in headers:
            raise IMAPException(f'Can\'t find letter #{number+1}')

        sender, receiver, subject, date = self.parse_headers(headers)

        sock.send(f'A{counter+1} FETCH {number+1} RFC822.SIZE\r\n'.encode())
        data = sock.recv(1024).decode()
        size = self.size_regex.findall(data)[0]

        return sender, receiver, subject, date, size

    def get_message_attachments(self, sock, number, counter):
        sock.send(f'A{counter} FETCH {number+1} BODYSTRUCTURE\r\n'.encode())
        data = bytearray()
        try:
            while True:
                received_data = sock.recv(1024)
                data.extend(received_data)
                if b'OK FETCH done\r\n' in received_data:
                    break
        except timeout:
            pass

        data = data.decode()
        attachments = self.attachment_regex.findall(data)
        return attachments

    @staticmethod
    def get_messages_numbers(use_all: bool, mails: int, mail_range: range):
        numbers = [i for i in range(mails)]

        if use_all:
            return numbers

        end_index = mail_range.stop
        start_index = mail_range.start

        existing_numbers = []
        for i in range(start_index, end_index + 1):
            if i in numbers:
                existing_numbers.append(i)
        if len(existing_numbers) != 0:
            return existing_numbers

        return -1

