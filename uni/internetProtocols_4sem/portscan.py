from argparse import ArgumentParser
from typing import List
import socket
from queue import Queue
from threading import Thread, Lock


class Scanner:
    def __init__(self, host_name: str, is_tcp: bool, ports_range: List[int]):
        try:
            self.host = socket.gethostbyname(host_name)
        except socket.gaierror:
            raise Exception('Unknown host\'s name')
        if not self.check_ports_range(ports_range):
            raise Exception('Wrong ports range')
        self.is_tcp = is_tcp
        self.print_lock = Lock()
        self.ports = Queue()
        for port in range(ports_range[0], ports_range[1] + 1):
            self.ports.put(port)

    @staticmethod
    def check_ports_range(ports_range: List[int]) -> bool:
        return (-1 < ports_range[0] <= ports_range[1] < 2 ** 16
                and len(ports_range) == 2)

    @staticmethod
    def get_app_protocol(port: int, trans_protocol: str) -> str:
        try:
            return socket.getservbyport(port, trans_protocol).upper()
        except OSError:
            return ''

    def scan_ports(self):
        while True:
            port = self.ports.get()
            self.scan_port(port)
            self.ports.task_done()

    def scan_port(self, port: int):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.settimeout(1)
                r = sock.connect_ex((self.host, port))
                if r == 0:
                    service = self.get_app_protocol(port, 'tcp')
                    with self.print_lock:
                        print(f'TCP {port} {service}')
            except (socket.timeout, ConnectionRefusedError):
                pass

    def run(self):
        if self.is_tcp:
            for _ in range(512):
                Thread(target=self.scan_ports, daemon=True).start()
            self.ports.join()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('host_name', help='Host for scanning')
    parser.add_argument('-t', action='store_true', dest='is_tcp')
    parser.add_argument('-p', '--ports', nargs='+', type=int, default=[0, 80], dest='ports_range')

    args = parser.parse_args().__dict__
    try:
        scanner = Scanner(**args)
        scanner.run()
    except Exception as e:
        print(e)