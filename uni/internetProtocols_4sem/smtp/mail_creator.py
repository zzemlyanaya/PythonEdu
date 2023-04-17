from smtp.utils import SMTPFile


class HideousMailCreator:
    def __init__(self):
        self.boundary = 'hideous'
        self.mail = ''

    def add_header(self, login_from: str, to: str, subject: str):
        self.mail += f'From: {login_from}\n' \
                     f'To: {to}\n' \
                     f'Subject: {subject}\n'\
                     f'Content-Type: multipart/mixed; boundary={self.boundary}' \
                     f'\n\n--{self.boundary}' \
                     f'\nContent-Type: text/plain; charset="utf-8"' \
                     '\nContent-Transfer-Encoding: quoted-printable\n\n' \
                     f'\nКотики!'

    def add_attachment(self, file: SMTPFile, is_last: bool):
        self.mail += f'\n\n--{self.boundary}'\
                     f'\nMime-Version: 1.0'\
                     f'\nContent-Type: image/{file.extension}; ' \
                     f'name="=?UTF-8?B?{file.encoded_name}?="'\
                     f'\nContent-Disposition: attachment; ' \
                     f'filename="=?UTF-8?B?{file.encoded_name}?="'\
                     '\nContent-Transfer-Encoding: base64\n\n'

        self.mail += file.get_encoded()
        self.mail += f'\n--{self.boundary}'
        if is_last:
            self.mail += '--'

    def get_mail(self):
        return f'{self.mail}\n.\n'

