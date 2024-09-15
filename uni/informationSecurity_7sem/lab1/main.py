import argparse
from enum import Enum

from HideousEncrypter import HideousEncrypter
from HideousEncrypter import EncrypterArgs


class HideousAction(Enum):
    PREPARE = 0
    ENCODE = 1
    TRANSLATE = 2
    DECODE = 3


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--picture', type=str, default='berry.jpeg', dest='pic_name')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = get_args()
        server_args = EncrypterArgs(args.pic_name, False)
        encrypter = HideousEncrypter(server_args)

        while True:
            action = HideousAction.__getitem__(input('Enter action: ').upper())
            if action == HideousAction.PREPARE:
                encrypter.extend()
            elif action == HideousAction.ENCODE:
                encrypter.encode()
            elif action == HideousAction.TRANSLATE:
                encrypter.translate()
            elif action == HideousAction.DECODE:
                encrypter.decode()
            else:
                print('Unknown action')
    except PermissionError:
        print('Not enough rights. Try sudo or run as admin')
        exit(1)
