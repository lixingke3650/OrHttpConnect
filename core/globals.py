#! usr/bin/python
# -*- coding: utf-8 -*-
# Filename: globals.py

# logger
G_Log = None
# log 文件名
G_LOG_NAME = 'httpconnect'
# log 输出级别
G_LOG_LEVEL = 'DEBUG'
# socket一次读取最大size
G_SOCKET_RECV_MAXSIZE = 65535
# 目标应用地址
G_TARGET_HOST = '0.0.0.0'
# 目标应用端口
G_TARGET_PORT = 0
# 监视IP
G_LISTEN_HOST = '0.0.0.0'
# 监视端口
G_LISTEN_PORT = 0
# 最大连接数
G_LISTEN_CONNECT_MAXNUMBER = 10
# HTTP Proxy IP
G_HTTPPROXY_HOST = '0.0.0.0'
# HTTP Proxy 端口
G_HTTPPROXY_PORT = 0
# HTTP Proxy认证控制 0 不认证/ 1 认证
G_HTTPPROXY_AUTH = 0
# HTTP Proxy 用户ID
G_HTTPPROXY_ID = 'lixingke3650'
# HTTP Proxy 密码
G_HTTPPROXY_PW = 'password'
# CONNECT请求用字符串
G_CONNECT_REQUEST = 'CONNECT ' + G_TARGET_HOST + ':' + str(G_TARGET_PORT) + ' HTTP/1.1\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\nContent-Length: 0\r\n\r\n'
# CONNECT 成功应答特征字符串
G_CONNECT_RESPONSE_OK = '200 Connection established' # HTTP/1.0 200 Connection established
# CONNECT 权限验证失败特征字符串
G_CONNECT_RESPONSE_UNAUTHORIZED = 'Unauthorized'