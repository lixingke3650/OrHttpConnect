#! usr/bin/python
# -*- coding: utf-8 -*-
# Filename: globals.py

__all__ = [ \
    'G_Log', 'G_LOG_NAME', 'G_LOG_LEVEL', 'G_HTTPPROXY_HOST', \
    'G_SOCKET_RECV_MAXSIZE', 'G_TARGET_HOST', 'G_TARGET_PORT', \
    'G_LISTEN_HOST', 'G_LISTEN_PORT', 'G_LISTEN_CONNECT_MAXNUMBER', \
    'G_HTTPPROXY_HOST', 'G_HTTPPROXY_PORT', 'G_HTTPPROXY_AUTH', \
    'G_HTTPPROXY_ID', 'G_HTTPPROXY_PW', 'G_CONNECT_REQUEST', \
    'G_CONNECT_REQUEST_SIGN', 'G_CONNECT_RESPONSE_OK', \
    'G_CONNECT_RESPONSE_UNAUTHORIZED' \
]

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
# CONNECT lixingke3650.info.tm:80 HTTP/1.1\r\nHost: lixingke3650.info.tm\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\nProxy-Authorization: Basic *\r\nContent-Length: 0\r\n\r\n
G_CONNECT_REQUEST = ''
G_CONNECT_REQUEST_SIGN = ''
# CONNECT 成功应答特征字符串
G_CONNECT_RESPONSE_OK = '200 Connection established' # HTTP/1.0 200 Connection established
# CONNECT 权限验证失败特征字符串
G_CONNECT_RESPONSE_UNAUTHORIZED = 'Unauthorized'