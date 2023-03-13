import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # host = 'urgu.org'
    # host = "webcode.me"
    # host = 'time.nist.gov'
    host = 'time.nist.gov'
    port = 13

    s.connect((host, port))

    m_str = "HEAD / HTTP/1.1\r\nHost: {}\nAccept: text/html\r\n\r\n".format(host)
    # m_str = ""
    msg = bytearray(m_str.encode())

    s.sendall(msg)
    answ = s.recv(4096)
    print(answ.decode('utf8'))
    
## следующее задание:
 #- получить ответ от  ресурса с такими данными 
 #   host = 'time.nist.gov'
 #   port = 13
  #  послать нужно пустую строку в запросе