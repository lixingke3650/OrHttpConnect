#! C:\Python\Python3\python
# -*- coding: utf-8 -*-
# FileName: HCService.py

# STD
import queue

# ORG
from . import globals
from . import ListenService
from . import PostService

class HCService():
    '''
    服务入口
    '''

    # 等待开启的HttpConnect服务队列
    _HCQueue = None
    # 监听服务
    _ListenService = None
    # 通信服务
    _PostService = None

    def __init__ (self, maxdate=globals.G_LISTEN_CONNECT_MAXNUMBER):
        '''
        初始化
        maxdata： 最大HttpConnect服务开启数
        '''

        self._HCQueue = queue.Queue(maxdate)
        self._ListenService = ListenService.ListenService(globals.G_LISTEN_IP, globals.G_LISTEN_PORT, self._HCQueue, maxdate)
        self._PostService = PostService.PostService(globals.G_HTTPPROXY_IP, globals.G_HTTPPROXY_PORT, self._HCQueue)

    def start(self):
        '''
        HttpConnect服务启动
        '''

        globals.G_Log.debug('HCService start! [ListenService.py:HCService:start]')
        self._PostService.start()

        if (self._ListenService.start() != True):
            globals.G_Log.error( 'Listen Service Start error! [HCService.py:HCService:start]' )
            return False
        elif (self._PostService.start() != True):
            globals.G_Log.error( 'Post Service Start error! [HCService.py:HCService:start]' )
            return False

        return True

    def stop(self):
        '''
        HttpConnect服务停止
        '''

        globals.G_Log.debug('HCService stop! [ListenService.py:HCService:stop]')
        if (self._ListenService.stop() != True):
            globals.G_Log.error( 'Listen Service Stop error! [HCService.py:HCService:stop]' )
            return False
        elif (self._PostService.stop() != True):
            globals.G_Log.error( 'Post Service Stop error! [HCService.py:HCService:stop]' )
            return False

        return True

