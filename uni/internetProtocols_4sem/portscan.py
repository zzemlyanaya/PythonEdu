from argparse import ArgumentParser
from dataclasses import dataclass
import socket
import time
import binascii
import re
from queue import Queue
from queue import Empty
from threading import Thread, RLock

protocol_names = {socket.SOCK_STREAM: 'TCP', socket.SOCK_DGRAM: 'UDP'}


@dataclass
class ScannerArgs:
    host: str
    scan_tcp: bool
    scan_udp: bool
    port_range: range


class HideousScanner:
    def __init__(self, args: ScannerArgs, threads=1000, timeout=3):
        self.ip = socket.gethostbyname(args.host)
        self.ports = args.port_range
        self.protocols = []
        if args.scan_tcp:
            self.protocols.append(socket.SOCK_STREAM)
        if args.scan_udp:
            self.protocols.append(socket.SOCK_DGRAM)

        self.lock = RLock()
        self.threads = threads

        self.q = Queue(maxsize=self.threads * 3)
        self.scan_data = ((self.ip, port, protocol) for port in self.ports for protocol in self.protocols)
        self.timeout = timeout
        self.scan_results = []

    def fill_queue(self):
        while True:
            if not self.q.full():
                try:
                    self.q.put(next(self.scan_data))
                except StopIteration:
                    break
            else:
                time.sleep(0.01)

    def worker(self):
        while True:
            try:
                data = self.q.get()
                if data[2] == socket.SOCK_STREAM:
                    self.ping_tcp(*data)
                else:
                    self.ping_udp(*data)
            except Empty:
                return
            finally:
                self.q.task_done()

    def ping_tcp(self, ip, port, protocol):
        with socket.socket(socket.AF_INET, protocol) as sock:
            sock.settimeout(self.timeout)
            status = sock.connect_ex((ip, port))
            if status == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = ''
                finally:
                    self.print_result(protocol, port, service)
                    self.scan_results.append((ip, port, protocol))

    def ping_udp(self, ip, port, protocol):
        with socket.socket(socket.AF_INET, protocol) as sock:
            sock.settimeout(self.timeout)
            try:
                sock.sendto(b'ping', (ip, port))
                data, _ = sock.recvfrom(1024)
                # ICMP (3,3) response = closed
                if data.startswith(bytes([3, 3])):
                    return
            except socket.timeout:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = ''
                finally:
                    self.print_result(protocol, port, service)
                    self.scan_results.append((ip, port, protocol))
            except socket.error:
                return

    def print_result(self, protocol, port, service):
        with self.lock:
            print('{} {} {}'.format(protocol_names[protocol], port, service))

    def run(self):
        queue_thread = Thread(target=self.fill_queue)
        queue_thread.daemon = True
        queue_thread.start()

        self.scan_results = []
        for i in range(self.threads):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

        self.q.join()
        return self.scan_results


def get_args():
    parser = ArgumentParser()
    parser.add_argument('host', type=str, default='localhost')
    parser.add_argument('-t', action='store_true', dest='scan_tcp', default=False)
    parser.add_argument('-u', action='store_true', dest='scan_udp', default=False)
    parser.add_argument('-p', '--ports', nargs='+', type=int, default=[0, 1023], dest='port_range')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = get_args()
        if args.port_range[0] > args.port_range[1] or args.port_range[1] > 65535:
            print('Incorrect ports')
            exit(1)

        if args.scan_udp and args.port_range[0] == 0:
            args.port_range[0] += 1

        ports = range(args.port_range[0], args.port_range[1] + 1)
        scan_args = ScannerArgs(args.host, args.scan_tcp, args.scan_udp, ports)
        scanner = HideousScanner(scan_args)
        scanner.run()
    except PermissionError:
        print('Not enough rights. Try sudo or run as admin')
        exit(1)

# 45.33.32.156
# ya.ru
# github.com
