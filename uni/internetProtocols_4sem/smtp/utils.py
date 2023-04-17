import base64
from pathlib import Path
from dataclasses import dataclass


class SMTPFile:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.extension = path.suffix[1:]
        self.encoded_name = base64.b64encode(path.name.encode('utf-8')).decode('utf-8')

    def get_encoded(self):
        with open(self.path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')


@dataclass
class SMTPAnswer:
    full_answer: str
    code: int
    message: str

    @staticmethod
    def from_str(msg: str):
        answer = msg
        if msg == '':
            return SMTPAnswer(answer, 0, '')
        parts = msg.split('\n')[:-1]
        last_code = int(parts[-1][0:4])
        last_message = parts[-1][5:]
        return SMTPAnswer(answer, last_code, last_message)

    def __str__(self):
        return self.full_answer


class SMTPException(Exception):
    def __init__(self, msg: str):
        self.msg = msg
