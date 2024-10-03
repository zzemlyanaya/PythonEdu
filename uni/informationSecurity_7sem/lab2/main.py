import argparse

from HideousEncrypter import EncrypterArgs
from HideousEncrypter import HideousEncrypter


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--doc', type=str, default='test.docx', dest='doc_name')
    parser.add_argument('-x', type=float, default=0.99, dest='x')
    parser.add_argument('-r', action='store_true', default=False, dest='reversed')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = get_args()
        server_args = EncrypterArgs(args.doc_name, args.x)
        encrypter = HideousEncrypter(server_args)
        if args.reversed:
            encrypter.decode()
        else:
            encrypter.work()
    except PermissionError:
        print('Not enough rights. Try sudo or run as admin')
        exit(1)
    except RuntimeError as e:
        print(e)
        exit(1)

