import argparse
import datetime
import socket
import struct
from multiprocessing.pool import ThreadPool
from dataclasses import dataclass

threads = 12
buffer = 1024
epoch = datetime.datetime(1900, 1, 1)


@dataclass
class ServerArgs:
    host: str
    delay: int
    port: int


# LI VN режим | слой
# регистрация | точность | задержка
# дисперсия | идентификатор эталон
# fake_begin_time | input_time | time_received
def pack(received, time_received, server_args):
    return struct.pack('!B', (0 << 6 | 3 << 3 | 4)) + struct.pack('!B', 1) \
           + struct.pack('!b', 0) + struct.pack('!b', -20) + struct.pack('!i', 0) \
           + struct.pack('!i', 0) + struct.pack('!i', 0) \
           + get_fake_time(server_args) + received[40:48] + time_received


def get_fake_time(server_args):
    time = (datetime.datetime.utcnow() - epoch).total_seconds() + server_args.delay
    sec, millisec = [int(x) for x in str(time).split('.')]
    return struct.pack('!II', sec, millisec)


def answer(server, received, addr, server_args):
    answer = pack(received, get_fake_time(server_args), server_args)
    server.sendto(answer + get_fake_time(server_args), addr)


def hideous_server(server_args):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((server_args.host, server_args.port))

    while True:
        data, addr = server.recvfrom(buffer)
        print(f'{addr} accept to {server_args.host}:{server_args.port}')
        ThreadPool(threads).apply_async(answer, args=(server, data, addr, server_args))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delay', type=int, default=0)
    parser.add_argument('-p', '--port', type=int, default=123)
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = get_args()
        server_args = ServerArgs('127.0.0.1', args.delay, args.port)
        hideous_server(server_args)
    except PermissionError:
        print('Not enough rights. Try sudo or run as admin')
        exit(1)
