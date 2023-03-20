import socket
import struct
import os
import time
import re
import random
from dataclasses import dataclass
from ipaddress import ip_address
import argparse

ICMP_ECHO_REQUEST = 8
WHOIS_SERVERS = ['whois.ripe.net', 'whois.arin.net', 'whois.apnic.net', 'whois.afrinic.net', 'whois.lacnic.net',
                 'whois.internic.net', 'whois.iana.org']


@dataclass
class IcmpPack:
    packet_type: int
    code: int

    def checksum(self, data):
        csum = 0
        countTo = (len(data) // 2) * 2

        for count in range(0, countTo, 2):
            thisVal = data[count + 1] * 256 + data[count]
            csum = csum + thisVal
            csum = csum & 0xffffffff

        if countTo < len(data):
            csum = csum + data[-1]
            csum = csum & 0xffffffff

        csum = (csum >> 16) + (csum & 0xffff)
        csum = csum + (csum >> 16)
        answer = ~csum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

    def __bytes__(self):
        checksum = 0
        # on darwin we need to do &
        myID = os.getpid() & 0xffff

        # fake header to calculate the checksum
        header = struct.pack('2B3H', self.packet_type, self.code, checksum, myID, 1)
        data = struct.pack("d", time.time())

        checksum = self.checksum(header + data)
        checksum = socket.htons(checksum) & 0xffff

        # real header
        header = struct.pack('2B3H', self.packet_type, self.code, checksum, myID, 1)
        packet = header + data
        return packet

    @staticmethod
    def from_bytes(data: bytes):
        return IcmpPack(*struct.unpack('BB', data[:2]))

    def is_echo_reply(self):
        return self.code == self.packet_type == 0


@dataclass
class TraceResult:
    destination: str
    num: int
    net_name: str
    as_zone: str
    country: str
    is_local: bool

    @staticmethod
    def from_whois_data(destination, num, data):
        is_local = data is None or 'EU' in data.get('country', '')
        country = data.get('country', '') if not is_local else ''
        country = country if country.lower() != 'eu' else ''
        as_zone = data.get('origin', '') if not is_local else ''
        netname = data.get('netname', '') if not is_local else ''
        return TraceResult(destination, num, netname, as_zone, country, is_local)

    def __str__(self):
        result = f'{self.num}. {self.destination}\r\n'
        if self.is_local:
            return result + 'local\r\n'
        info = []
        if self.net_name:
            info.append(self.net_name)
        if self.as_zone:
            info.append(self.as_zone)
        if self.country:
            info.append(self.country)
        return result + ', '.join(info) + '\r\n'


def query_whois_servers(addr):
    if ip_address(addr).is_private:
        return ''

    for server in WHOIS_SERVERS:
        res = query_server(server, addr)
        if res:
            return res
        else:
            continue
    return ''


def query_server(server, addr):
    print('query ' + server + ' on ' + addr)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as whois_sock:
        whois_sock.settimeout(5)
        whois_sock.connect((socket.gethostbyname(server), 43))
        whois_sock.send(addr.encode(encoding='utf-8') + b'\r\n')
        try:
            data = bytearray()
            while True:
                temp_data = whois_sock.recv(1024)
                if not temp_data:
                    break
                data.extend(temp_data)

            decoded = data.decode()
            if 'No match' in decoded or 'block not managed by' in decoded:
                return ''
            else:
                return decoded
        except (socket.timeout, UnicodeDecodeError, ValueError, socket.gaierror):
            return ''


def get_whois_data(addr: str):
    data = query_whois_servers(addr)

    if not data:
        return {}

    whois_data = {}

    for field in ('netname', 'country', 'origin'):
        try:
            field_start = data.index(field)
            field_end = data.index('\n', field_start)
            key_value_data = data[field_start:field_end]
            field_data = key_value_data.replace(' ', '').split(':')[1]
            whois_data[field] = field_data
        except ValueError:
            continue
    return whois_data


def trace(address):
    ttl = 1
    timeout = 15
    max_hops = 30

    try:
        address = socket.gethostbyname(address)
    except socket.gaierror:
        print('Wrong address to traceroute')
        exit(1)

    success_num = 1

    if address == socket.gethostbyname('localhost'):
        max_hops = 1

    while ttl <= max_hops:
        sock_receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock_receiver.settimeout(timeout)

        sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
        sock_sender.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
        sock_sender.sendto(IcmpPack(ICMP_ECHO_REQUEST, 0).__bytes__(), (address, 80))

        try:
            data, conn = sock_receiver.recvfrom(1024)
            whois_data = get_whois_data(conn[0])
            icmp_response = IcmpPack.from_bytes(data[20:])
            trace_result = TraceResult.from_whois_data(conn[0], success_num, whois_data)
            success_num += 1
            yield trace_result

            if icmp_response.is_echo_reply():
                sock_sender.close()
                sock_receiver.close()
                break
        except socket.timeout:
            yield '* * * Request timeout'
            pass
        finally:
            ttl += 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('destination')
    return parser.parse_args().__dict__


if __name__ == '__main__':
    args = parse_args()
    host = args.pop('destination')
    try:
        for res in trace(host):
            print(res, end='\r\n')
    except PermissionError:
        print('Not enough rights. Try sudo or run as admin')
        exit(1)
