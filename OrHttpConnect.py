#! C:\Python\Python3\python
# -*-conding: utf-8 -*-
# FileName: OrHttpConnect.py

# STD

# ORG
from Tools import *
from core import *
# import hello

# 版本说明
# 0.01：新建
__Version__ = '0.01'


_OrHttpConnectService = None

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
    return True

def main():
    IO.printX ('hello!')

    ret = init()
    IO.printX ('init: ' + str(ret))

    ret = start()
    IO.printX ('start: ' + str(ret))

    # ret = stop()
    # IO.printX ('stop: ' + str(ret))


if __name__ == '__main__':
    globals.G_Log = Logger.getLogger('test.log')
    globals.G_Log.error('hello logger')

    main()

    # hello.hello()