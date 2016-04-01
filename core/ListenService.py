#! C:\Python\Python2\python
# -*-coding: utf-8-*-
# FileName: ListenService.py

# STD
import socket
import threading
import queue

# ORG
# from Tool import *
from . import globals
from . import HCWorker

class ListenService():
    """ListenService服务
    监听本地连接，并读取数据存放到队列中"""

    # 数据队列
    _HCQueue = None
    # 监听服务socket
    _ServiceSocket = None
    # 监听地址
    _ServerAddress = None
    # 监听连接最大数
    _ConnectMaximum = None
    # 监听进程描述符
    _GeneratorThread = None
    # 监听服务启动标识
    _isRun = None
    # 监听服务子通信进程维护列表

    def __init__(self, ip, port, hcqueue, maximum):
        '''监听服务初始化'''

        self._HCQueue = hcqueue
        self._ServerAddress = (ip, port)
        self._ConnectMaximum = maximum
        self._isRun = False

    def start(self):
        '''监听服务启动'''

        globals.G_Log.debug('listen start! [ListenService.py:ListenService:start]')
        if (self._HCQueue == None):
            return False
        try:
            self._ServiceSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self._ServiceSocket.bind( self._ServerAddress )
            self._ServiceSocket.listen( self._ConnectMaximum )
            self._GeneratorThread = threading.Thread( target = self.generator )
            self._isRun = True
            self._GeneratorThread.start()
            return True
        except Exception as e:
            globals.G_Log.error( 'Listen Service Start error! [ListenService.py:ListenService:start] --> %s' %e )

    def stop(self):
        '''监听服务停止'''

        globals.G_Log.debug('listen stop! [ListenService.py:ListenService:stop]')
        if (self._isRun == False):
            return True
        try:
            self._ServiceSocket.shutdown( socket.SHUT_RDWR )
            self._ServiceSocket.close()
            self._ServiceSocket = None
            self._isRun = False
            self._GeneratorThread.jion(10)
            return True
        except Exception as e:
            globals.G_Log.error( 'Listen Service Stop error! [ListenService.py:ListenService:stop] --> %s' %e )
            return False

    def generator(self):
        '''监听等待并分发处理 accept'''

        globals.G_Log.debug('listen generator start! [ListenService.py:ListenService:generator]')
        while (self._isRun == True):
            try:
                sock, address = self._ServiceSocket.accept()
                hcworker = HCWorker.HCWorker()
                hcworker._HC_App_Socket = sock
                hcworker._Connect_Request = globals.G_CONNECT_REQUEST

                # connect 尝试
                # 放入PostService中进行，参考PostService.py:connecttry()

                # worker加入到队列
                self._HCQueue.put(hcworker)
            except Exception as e:
                globals.G_Log.error( 'listen generator error! [ListenService.py:ListenService:generator] --> %s' %e )
