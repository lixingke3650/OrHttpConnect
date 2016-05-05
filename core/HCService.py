#! C:\Python\Python3\python
# -*- coding: utf-8 -*-
# FileName: HCService.py

# STD
import queue

# ORG
from . import globals
from core.ListenService import *
from core.PostService import *

__all__ = ['HCService']

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
    # 通信列表
    _WorkList = []

    def __init__ (self, maxdate=globals.G_LISTEN_CONNECT_MAXNUMBER):
        '''
        初始化
        maxdata： 最大HttpConnect服务开启数
        '''

        self._HCQueue = queue.Queue(maxdate)
        self._ListenService = ListenService(globals.G_LISTEN_HOST, globals.G_LISTEN_PORT, self._HCQueue, maxdate)
        self._PostService = PostService(globals.G_HTTPPROXY_HOST, globals.G_HTTPPROXY_PORT, self._HCQueue, self._WorkList)

    def start(self):
        '''
        HttpConnect服务启动
        '''

        globals.G_Log.debug('HCService start! [ListenService.py:HCService:start]')

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
        ret = True
        if (self._PostService.stop() != True):
            globals.G_Log.error( 'Post Service Stop error! [HCService.py:HCService:stop]' )
            ret = ret and False
        if (self._ListenService.stop() != True):
            globals.G_Log.error( 'Listen Service Stop error! [HCService.py:HCService:stop]' )
            ret = ret and False

        return ret

