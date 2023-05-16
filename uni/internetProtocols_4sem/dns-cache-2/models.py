import struct
from utils import get_qname_bytes, bytes_at


class DNSQuery:
    def __init__(self, qname: str, qtype: int, qclass: int):
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass

    def to_bytes(self):
        name, size = get_qname_bytes(self.qname)
        bytes_query = struct.pack("!" + str(size) + 's2h', name, self.qtype, self.qclass)
        return bytes_query, size + 4


class DNSHeader:
    def __init__(self,
                 id: int,
                 qr: bool = 1, opcode: int = 0, aa: bool = True, tc: bool = False,
                 rd: bool = True, ra: bool = True,
                 rcode: int = 0, qd_count: int = 0, an_count: int = 0,
                 ns_count: int = 0, ar_count: int = 0):
        self.id = id
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.rcode = rcode
        self.qd_count = qd_count
        self.an_count = an_count
        self.ns_count = ns_count
        self.ar_count = ar_count

    def to_bytes(self):
        qr_rcode = (self.qr << 15 | (self.opcode & 0b1111) << 11 |
                    self.aa << 10 | self.tc << 9 | self.rd << 8 |
                    self.ra << 7 | (self.rcode & 0b1111))

        return struct.pack('!hH4h', self.id, qr_rcode,
                           self.qd_count, self.an_count,
                           self.ns_count, self.ar_count)

    @staticmethod
    def parse_header(header_bytes):
        lines = struct.unpack('!6h', header_bytes)

        return DNSHeader(
            id=lines[0],

            qr=bytes_at(lines[1], 15, 1),
            opcode=bytes_at(lines[1], 11, 4),
            aa=bytes_at(lines[1], 10, 1),
            tc=bytes_at(lines[1], 9, 1),
            rd=bytes_at(lines[1], 8, 1),
            ra=bytes_at(lines[1], 7, 1),
            rcode=bytes_at(lines[1], 0, 1),

            qd_count=lines[2],
            an_count=lines[3],
            ns_count=lines[4],
            ar_count=lines[5])


class DNSPackage:
    def __init__(self, header: DNSHeader):
        self.header: DNSHeader = header
        self.queries = []
        self.ans_records = []
        self.auth_records = []
        self.additional_records = []

    def add_query(self, query: DNSQuery):
        self.queries.append(query)
        return self

    def set_payload(self, queries, records):
        self.queries = queries
        self.ans_records = records[:self.header.an_count]
        self.auth_records = records[self.header.an_count:self.header.an_count + self.header.ns_count]
        self.additional_records = records[self.header.an_count + self.header.ns_count:self.header.an_count + self.header.ns_count + self.header.ar_count]
        return self

    def to_bytes(self) -> bytes:
        format = '!12s'
        values = [self.header.to_bytes()]
        for q in self.queries:
            query_bytes, size = q.to_bytes()
            format += str(size) + 's'
            values.append(query_bytes)
        for r in self.ans_records + self.auth_records + self.additional_records:
            record_bytes = r.to_bytes()
            format += str(len(record_bytes)) + 's'
            values.append(record_bytes)

        return struct.pack(format, *values)


class ResourceRecord:
    def __init__(self, name: str, rtype: int, rclass: int, ttl: int, rd_length: int, rdata: bytes):
        self.name = name
        self.rtype = rtype
        self.rclass = rclass
        self.ttl = ttl
        self.rd_length = rd_length
        self.rdata = rdata

    def to_bytes(self) -> bytes:
        name, size = get_qname_bytes(self.name)
        return struct.pack(
            '!' + str(size) + 's2hIH' + str(self.rd_length) + 's',
            name, self.rtype, self.rclass, self.ttl, self.rd_length, self.rdata)

    def __eq__(self, other):
        return self.name == other.name and self.rtype == other.rtype and \
               self.rclass == other.rclass and self.ttl == other.ttl and \
               self.rd_length == other.rd_length and self.rdata == other.rdata


def create_dns_package(request_id: int, queries) -> DNSPackage:
    header = DNSHeader(request_id, False, 0, False, False, True, True, 0, 1, 0, 0, 0)
    return DNSPackage(header).set_payload(queries, [])


def parse_request(data: bytes) -> DNSPackage:
    header, queries = struct.unpack('!12s' + str(len(data) - 12) + 's', data)
    header = DNSHeader.parse_header(header)
    queries, records = parse_queries(queries, header.qd_count, data)
    records = list(parse_records(records, data))
    return DNSPackage(header).set_payload(queries, records)


def parse_queries(queries_bytes: bytes, query_count: int, body: bytes):
    queries = []
    for i in range(query_count):
        qname, queries_bytes = read_domain(queries_bytes, body)
        qtype: int = struct.unpack('!h', queries_bytes[:2])[0]
        qclass: int = struct.unpack('!h', queries_bytes[2:4])[0]
        queries_bytes = queries_bytes[4:]

        queries.append(DNSQuery(qname, qtype, qclass))
    return queries, queries_bytes


def read_domain(queries_bytes, body: bytes):
    labels = []
    lsize = queries_bytes[0]
    queries_bytes = queries_bytes[1:]
    while lsize > 0:
        if lsize & 0b1100_0000:
            ptr = (lsize ^ 0b1100_0000) << 8 | queries_bytes[0]
            queries_bytes = queries_bytes[1:]
            subqname, _ = read_domain(body[ptr:], body)
            labels.append(subqname)
            break
        labels.append(queries_bytes[:lsize].decode(encoding='cp1251'))
        queries_bytes = queries_bytes[lsize:]
        lsize = queries_bytes[0]
        queries_bytes = queries_bytes[1:]
    qname = '.'.join(labels)
    return qname, queries_bytes


def parse_records(records: bytes, body: bytes):
    while len(records) > 0:
        record, records = parse_record(records, body)
        yield record


def parse_record(record_bytes: bytes, body: bytes):
    domain, residual = read_domain(record_bytes, body)
    # 10 is 2*2+4+2
    rtype, rclass, ttl, rdlength, data = struct.unpack('!2hIH' + str(len(residual) - 10) + 's', residual)
    rdata, next_record = struct.unpack('!' + str(rdlength) + 's' + str(len(data) - rdlength) + 's', data)

    record = ResourceRecord(domain, rtype, rclass, ttl, rdlength, rdata)
    return record, next_record
