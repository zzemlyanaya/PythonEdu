import socket, struct, sys, time

TIME1970 = 2208988800


def sntp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = '\x1b' + 47 * '\0'
    client.sendto(data.encode('utf-8'), ('127.0.0.1', 123))
    data, address = client.recvfrom(1024)
    if data:
        print('Response received from:', address)
    t = struct.unpack('!12I', data)[10] - TIME1970
    print('\tTime = %s' % time.ctime(t))
    client.close()


if __name__ == '__main__':
    while input() != "1":
        sntp_client()
