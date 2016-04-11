#! C:\Python\Python3\python
# -*-coding: utf-8-*-
# FileName: OrHttpConnect.py

# STD
import platform
# ORG
from Tools import *
from core import *

# 版本说明
# 0.01： 新建 基本功能实现
# 0.02： 追加配置文件功能，追加控制台信息输出(启动信息等)
__Version__ = '0.02'


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
    _OrHttpConnectService = HCService.HCService()
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
    IO.printX('* Listen Host: %s' % globals.G_LISTEN_HOST)
    IO.printX('* Listen Port: %d' % globals.G_LISTEN_PORT)
    IO.printX('* Target Host: %s' % globals.G_TARGET_HOST)
    IO.printX('* Target Port: %d' % globals.G_TARGET_PORT)
    IO.printX('* Log Level: %s' % globals.G_Log.getLevel())
    IO.printX('============================================================')
    IO.printX('')
    IO.printX('init():  ' + str(initret))

    startret = start()
    IO.printX ('start(): ' + str(startret))

    # ret = stop()
    # IO.printX ('stop: ' + str(ret))

if __name__ == '__main__':
    main()
