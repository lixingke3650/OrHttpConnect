#! C:\Python\Python3\python
# -*-coding: utf-8-*-
# FileName: OrHttpConnect.py

# STD
import platform
# ORG
from Tools import *
from core import *

# 版本说明
# 0.01： 新建 基本功能实现 (2016.03.31)
# 0.02： 追加配置文件功能，追加控制台信息输出(启动信息等) (2016.04.11)
# 0.03: 追加 HTTP Proxy 登陆验证, 追加work管理 (2016.04.13)
# 0.04: HTTP Proxy 登陆验证修正, import方式变更 (2016.04.26)
# 0.05: 服务stop修正
__Version__ = '0.05'


_OrHttpConnectService = None

def loadConfig():
    config = Config.ConfigIni('Config.ini')
    globals.G_LOG_NAME = config.getKey('OrHttpConnect','LOG_NAME')
    globals.G_LOG_LEVEL = config.getKey('OrHttpConnect','LOG_LEVEL')
    globals.G_HTTPPROXY_AUTH = config.getKeyInt('OrHttpConnect','HTTPPROXY_AUTH')
    if (globals.G_HTTPPROXY_AUTH == 1):
        globals.G_HTTPPROXY_ID = config.getKey('OrHttpConnect','HTTPPROXY_ID')
        globals.G_HTTPPROXY_PW = config.getKey('OrHttpConnect','HTTPPROXY_PW')
    globals.G_LISTEN_HOST = config.getKey('OrHttpConnect','LISTEN_HOST')
    globals.G_LISTEN_PORT = config.getKeyInt('OrHttpConnect','LISTEN_PORT')
    globals.G_HTTPPROXY_HOST = config.getKey('OrHttpConnect','HTTPPROXY_HOST')
    globals.G_HTTPPROXY_PORT = config.getKeyInt('OrHttpConnect','HTTPPROXY_PORT')
    globals.G_TARGET_HOST = config.getKey('OrHttpConnect','TARGET_HOST')
    globals.G_TARGET_PORT = config.getKeyInt('OrHttpConnect','TARGET_PORT')
    globals.G_LISTEN_CONNECT_MAXNUMBER = config.getKeyInt('OrHttpConnect','CONNECT_MAXNUMBER')

def globalsInit():
    globals.G_Log = Logger.getLogger(globals.G_LOG_NAME)
    globals.G_Log.setLevel(globals.G_LOG_LEVEL)
    # HTTP Proxy Connect请求生成
    globals.G_CONNECT_REQUEST = 'CONNECT ' + globals.G_TARGET_HOST + ':' + str(globals.G_TARGET_PORT) + \
                        ' HTTP/1.1\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\nContent-Length: 0\r\n\r\n'
    globals.G_CONNECT_REQUEST_SIGN = 'CONNECT ' + globals.G_TARGET_HOST + ':' + str(globals.G_TARGET_PORT) + \
                        ' HTTP/1.1\r\nProxy-Connection: Keep-Alive\r\nConnection: keep-alive\r\nProxy-Authorization: Basic ' + \
                        Coding.Base64.enBase64_s2s(globals.G_HTTPPROXY_ID + ':' + globals.G_HTTPPROXY_PW) + '\r\nContent-Length: 0\r\n\r\n'

def stop():
    global _OrHttpConnectService
    if (_OrHttpConnectService == None):
        return False

    if (True == _OrHttpConnectService.stop()):
        _OrHttpConnectService = None
        return True

    return False

def start():
    global _OrHttpConnectService
    _OrHttpConnectService = HCService()
    return _OrHttpConnectService.start()

def init():
    loadConfig()
    globalsInit()
    return True

def main():
    IO.printX('OrHttpConnect  (https://github.com/lixingke3650/OrHttpConnect)')
    IO.printX('Version: ' + __Version__)
    IO.printX('Python Version: %s (%s, %s)' %(platform.python_version(),platform.architecture()[0],platform.system()))
    IO.printX('')

    initret = init()

    IO.printX('============================================================')
    IO.printX('* HttpProxy Host: %s' % globals.G_HTTPPROXY_HOST)
    IO.printX('* HttpProxy Port: %d' % globals.G_HTTPPROXY_PORT)
    IO.printX('* HttpProxy Auth: %s' % globals.G_HTTPPROXY_AUTH)
    if (globals.G_HTTPPROXY_AUTH == 1 and globals.G_LOG_LEVEL == 'DEBUG'):
        IO.printX('* HttpProxy ID: %s' % globals.G_HTTPPROXY_ID)
        IO.printX('* HttpProxy PW: %s' % globals.G_HTTPPROXY_PW)
        IO.printX('* HttpProxy REQUEST_SIGN: %s' % globals.G_CONNECT_REQUEST_SIGN)
    IO.printX('* Listen Host: %s' % globals.G_LISTEN_HOST)
    IO.printX('* Listen Port: %d' % globals.G_LISTEN_PORT)
    IO.printX('* Target Host: %s' % globals.G_TARGET_HOST)
    IO.printX('* Target Port: %d' % globals.G_TARGET_PORT)
    IO.printX('* Log Level: %s' % globals.G_Log.getLevel())
    IO.printX('============================================================')
    IO.printX('')

    if (initret == True):
        IO.printX('init: Succeed.')
    else :
        IO.printX('init: Failed!')
        return False

    startret = start()
    if (startret == True):
        IO.printX ('start: Succeed.')
    else :
        IO.printX('start: Failed!')
        return False

    IO.printX('OrHttpConnect Service Started.')

    # stopret = stop()
    # if (stopret == True):
    #     IO.printX('stop: Succeed.')
    # else :
    #     IO.printX('stop: Failed!')
    #     return False

if __name__ == '__main__':
    main()
