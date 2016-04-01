#! usr/bin/python
# -*- coding: utf-8 -*-
# Filename: globals.py

# logger
G_Log = None
# log 文件名
G_LOG_NAME = 'httpconnect'
# log 输出级别
G_LOGLEVEL = 'INFO'
# socket一次读取最大size
G_SOCKET_RECV_MAXSIZE = 65535
# 目标应用地址
G_TARGET_HOST = '0.0.0.0'
# 目标应用端口
G_TARGET_PORT = 0
# 监视IP
G_LISTEN_IP = '127.0.0.1'
# 监视端口
G_LISTEN_PORT = 0
# 最大连接数
G_LISTEN_CONNECT_MAXNUMBER = 10
# HTTP Proxy IP
G_HTTPPROXY_IP = '0.0.0.0'
# HTTP Proxy 端口
G_HTTPPROXY_PORT = 8080
# CONNECT请求用字符串
# CONNECT lixingke3650.info.tm:80 HTTP/1.1\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\n\r\n
# CONNECT lixingke3650.info.tm:80 HTTP/1.1\r\nHost: lixingke3650.info.tm\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\n\r\n
G_CONNECT_REQUEST = 'CONNECT ' + G_TARGET_HOST + ':' + str(G_TARGET_PORT) + ' HTTP/1.1\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\n\r\n'
# CONNECT 成功应答特征字符串
G_CONNECT_RESPONSE_OK = '200 Connection established' # HTTP/1.0 200 Connection established
