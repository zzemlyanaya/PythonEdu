import argparse
import datetime
import socket
import struct
from dataclasses import dataclass
from HideousServer import HideousServer


@dataclass
class ScannerArgs:
    host: str
    scan_tcp: bool
    scan_udp: bool
    port_range: range


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--forwarder', type=str, default='8.8.8.8')
    parser.add_argument('-p', '--port', type=int, default=53)
    parser.add_argument('-h', '--help', action='store_true', dest='help_needed', default=False)
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = get_args()
        server_args = ServerArgs('127.0.0.1', args.delay, args.port)
        HideousServer(server_args)
    except PermissionError:
        print('Not enough rights. Try sudo or run as admin')
        exit(1)
