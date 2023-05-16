import socket
from argparse import ArgumentParser
from imap.imap_client import HideousClient
# from imap_client import HideousClient


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--ssl", action='store_true', help='Use ssl if supported by IMAP server. Default is False')
    parser.add_argument("-s", "--server", type=str, required=True, help='Address or domain of IMAP server to use')
    parser.add_argument("-u", "--user", type=str, help='User login')
    parser.add_argument('-n', nargs='+', type=int, default=[-1], dest='mails', help='Range of mails to print. Default is all')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    use_all = True
    mail_range = []
    if args.mails[0] != -1:
        use_all = False
        if args.mails[0] > args.mails[1]:
            raise ValueError('Incorrect mail range')
        mail_range = range(args.mails[0], args.mails[1] + 1)

    try:
        client = HideousClient(args.server, args.user, args.ssl, use_all, mail_range)
        client.run()
    except ValueError as e:
        print(e)
    except socket.gaierror:
        print('DNS Error')
    except ConnectionError:
        print('Connection error')
