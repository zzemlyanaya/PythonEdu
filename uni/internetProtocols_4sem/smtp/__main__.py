from _socket import gaierror
from argparse import ArgumentParser
from smtp.smtp_client import HideousClient


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--from', type=str, default='<>', dest='sender', help='Mailing address from')
    parser.add_argument('-t', '--to', type=str, help='Mailing address to')
    parser.add_argument('-d', '--directory', type=str, default='.', help='Image directory')
    parser.add_argument('--subject', type=str, default='Happy pictures',
                        help='Subject of the email, optional. Default subject is “Hello there”')
    parser.add_argument('-s', '--server', type=str, default='smtp.mail.ru:25',
                        help='Address or domain of SMTP server to use')
    parser.add_argument('--ssl', action='store_true',
                        help='Use ssl if supported by SMTP server. Default is False')
    parser.add_argument('--auth', action='store_true', help='Request authorization. Default if False')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print work log')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    try:
        client = HideousClient(args.sender, args.to, args.subject, args.directory, args.server, args.ssl, args.auth, args.verbose)
        client.run()
    except ValueError as e:
        print(e)
    except gaierror:
        print('DNS Error')
    except ConnectionError:
        print('Connection error')

#  python3 -m smtp -s smtp.yandex.ru:587 -f zemlyanayaek@ya.ru -t zemlyanayaek@ya.ru --verbose -d ./cats --auth --ssl
