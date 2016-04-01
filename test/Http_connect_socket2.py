#! C:\Python\Python2\python
# _*_ coding=utf-8 _*_
# Filename : Http_connect_socket2.py

import socket

# IP
CONNECT_IP = '0.0.0.0'
# port
CONNECT_PORT = 8080

# addr
Address = ( CONNECT_IP, CONNECT_PORT )
# socket
Socket_Client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
# connect
Socket_Client.connect( Address )
# data = 'CONNECT lixingke3650.info.tm:80 HTTP/1.1\r\nHost: lixingke3650.info.tm\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\n\r\n'
data = 'CONNECT lixingke3650.info.tm:80 HTTP/1.1\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\n\r\n'
Socket_Client.send(data.encode('utf8'))
res = Socket_Client.recv( 2048 )
print (res)

data = 'GET http://lixingke3650.info.tm HTTP/1.1\r\nHost: lixingke3650.info.tm\r\nAccept: image/png,image/*;q=0.8,*/*;q=0.5\r\nAccept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
Socket_Client.send(data.encode('utf8'))
res = Socket_Client.recv( 2048 )
print (res)
# while True:
#     res = Socket_Client.recv( 2048 )
#     print (res)