import time
import socket
from dataclasses import dataclass
from HideousCache import HideousCache
from models import DNSHeader, DNSPackage, parse_request, create_dns_package


@dataclass
class ServerArgs:
    host: str
    port: int
    forwarder: str
    cache: HideousCache


class HideousServer:
    def __init__(self, args: ServerArgs):
        self.address = args.host
        self.port = args.port
        self.forwarder = args.forwarder

        self.cache = args.cache
        self.last_id = 0

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('127.0.0.1', self.port))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(5)
        fwd_address = (self.forwarder, self.port)

        print('Server started')
        while True:
            request_bytes, address = server_socket.recvfrom(512)

            print(f'Received request from {address}')
            request = parse_request(request_bytes)

            have_non_cached_queries = False
            for q in request.queries:
                if (q.qname, q.qtype) not in self.cache:
                    have_non_cached_queries = True
                    break

            if have_non_cached_queries:
                print(f'\tNot found in cache. Forwarding to {self.forwarder}....')
                try:
                    client_socket.sendto(request_bytes, fwd_address)
                    dns_bytes, _ = client_socket.recvfrom(512)

                    print(f'\tReceived answer from {self.forwarder}')
                    dns_response = parse_request(dns_bytes)

                    if self.last_id == dns_response.header.id:
                        print(f'Found cyclic DNS request! Rejecting the request')
                        server_socket.sendto(
                            create_dns_package(request.header.id, request.queries).to_bytes(),
                            address)
                        continue

                    self.last_id = dns_response.header.id

                    now = time.time()

                    for rr in dns_response.ans_records + dns_response.auth_records + dns_response.additional_records:
                        key = (rr.name, rr.rtype)
                        self.cache.append(key, (rr, now))

                    server_socket.sendto(dns_bytes, address)
                    print(f'\tResponded to {address}')
                except:
                    server_socket.sendto(
                        create_dns_package(request.header.id, request.queries).to_bytes(),
                        address)
                    print('Forwarding server is unreachable')
            else:
                print('\tFound in cache!')
                rrs_with_time = []
                for q in request.queries:
                    key = (q.qname, q.qtype)
                    rrs_with_time += self.cache[key]

                rrs = list(map(lambda p: p[0], rrs_with_time))
                header = DNSHeader(request.header.id, True,
                                   qd_count=len(request.queries),
                                   an_count=len(rrs))
                response = DNSPackage(header)
                response.set_payload(request.queries, rrs)

                server_socket.sendto(response.to_bytes(), address)
                print(f'\tResponded to {address}')
