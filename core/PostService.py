#! C:\Python\Python2\python
# -*-coding: utf-8-*-
# FileName: PostService.py

# std
import socket
import threading

# org
from . import globals
from Tools import *

__all__ = ['PostService']


class PostService():
    """PostService
    数据发送服务(双向)"""

    # 数据队列
    _HCQueue = None
    # 发送进程描述符
    _PostThread = None
    # 发送目标地址(Http Proxy地址)
    _PostAddress = None
    # 运行标识
    _isRun = None
    # 送信服务列表
    _HCWorks = []
    # 送信服务列表维护用线程锁
    _HCWorkThreadRLock = None


    def __init__(self, ip, port, hcqueue, worklist):
        '''送信服务初始化'''

        self._HCQueue = hcqueue
        self._PostAddress = (ip, port)
        self._isRun = False
        self._HCWorkThreadRLock = threading.RLock()
        self._HCWorks = worklist

    def start(self):
        '''数据发送服务启动'''

        globals.G_Log.debug('post start! [PostService.py:PostService:start]')
        if (self._HCQueue == None):
            return False
        try:
            self._PostThread = threading.Thread( target = self.postrun )
            self._isRun = True
            self._PostThread.start()
            return True
        except Exception as e:
            globals.G_Log.error( 'Post Service Start error! [PostService.py:PostService:start] --> %s' %e )
            return False

    def stop(self):
        '''送信服务停止'''

        globals.G_Log.debug('post stop! [PostService.py:PostService:stop]')
        if (self._isRun == False):
            return True
        try:
            self._isRun = False
            # 列表中worker停止
            while worker in self._HCWorks:
                self.abolishworker(worker)
            self._PostThread.join(10)
            return True
        except Exception as e:
            globals.G_Log.error( 'Listen Service Stop error! [PostService.py:PostService:stop] --> %s' %e )
            return False

    def connecttry(self, worker):
        '''http connect连接'''

        globals.G_Log.debug('connecttry! [PostService.py:PostService:connecttry]')
        if (worker._IsConnect != False):
            return False
        try:
            if (globals.G_HTTPPROXY_AUTH == 1):
                # 验证proxy登录信息
                worker._HttpProxy_HC_Socket.send(globals.G_CONNECT_REQUEST_SIGN.encode('utf8'))
            else :
                # 不验证proxy登录信息
                worker._HttpProxy_HC_Socket.send(globals.G_CONNECT_REQUEST.encode('utf8'))
            resbytes = worker._HttpProxy_HC_Socket.recv( 128 )
            resstr = resbytes.decode('utf8')
            globals.G_Log.debug(resstr)
            ret = resstr.find( globals.G_CONNECT_RESPONSE_OK )
            if( ret == -1 ):
                return False
            return True
        except Exception as e:
            globals.G_Log.error( 'Post Service connecttry error! [PostService.py:PostService:connecttry] --> %s' %e )

    def postrun(self):
        '''数据发送(双向)'''

        globals.G_Log.debug('postrun! [PostService.py:PostService:postrun]')
        try:
            while (self._isRun == True):
                hcworker = self._HCQueue.get()
                launchthread = threading.Thread( target = self.launchworker, args = (hcworker,) )
                launchthread.start()
                
        except Exception as e:
            globals.G_Log.error( 'Post Service run error! [PostService.py:PostService:postrun] --> %s' %e )

    def launchworker(self, worker):
        '''开启一条通信作业
           首先尝试HTTP CONNECT，成功则启动收送信处理，失败则结束worker
        '''

        globals.G_Log.debug('launchworker! [PostService.py:PostService:launchworker]')
        try:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( self._PostAddress )
            worker._HttpProxy_HC_Socket = sock
            # connect
            if (True != self.connecttry(worker)) :
                globals.G_Log.info('HTTP CONNECT FAIL! [PostService.py:PostService:launchworker] --> IP: %s' %self._PostAddress)
                return False
            worker._IsConnect = True
            ctosthread = threading.Thread( target = self.ctosrun, args = (worker,) )
            stocthread = threading.Thread( target = self.stocrun, args = (worker,) )
            worker._CToSThread = ctosthread
            worker._SToCThread = stocthread
            ctosthread.start()
            stocthread.start()
            worker._IsEnable = True
            ret = self.worksmanager('add', worker)
            # LOG LEVEL是DEBUG时，输出运行信息
            if (globals.G_LOG_LEVEL == 'DEBUG'):
                IO.printX('worker add %d' %ret)
        except Exception as e:
            globals.G_Log.error( 'Worker Launch error! [PostService.py:PostService:launchworker] --> %s' %e )

    def abolishworker(self, worker):
        '''worker 停止
        '''

        globals.G_Log.debug('abolishworker! [PostService.py:PostService:abolishworker]')
        try:
            if (worker._IsEnable == True):
                if (worker._HttpProxy_HC_Socket != None):
                    worker._HttpProxy_HC_Socket.shutdown( socket.SHUT_RDWR )
                    worker._HttpProxy_HC_Socket.close()
                    worker._HttpProxy_HC_Socket = None
                if (worker._HC_App_Socket != None):
                    worker._HC_App_Socket.shutdown( socket.SHUT_RDWR )
                    worker._HC_App_Socket.close()
                    worker._HC_App_Socket = None
                try:
                    ret = self.worksmanager('del', worker)
                    worker._IsEnable = False
                    # LOG LEVEL是DEBUG时，输出运行信息
                    if (globals.G_LOG_LEVEL == 'DEBUG'):
                        IO.printX('worker del %d' %ret)
                except:
                    # tunnel worker delete error
                    # 可能存在多重删除的情况，输出DEBUG日志
                    globals.G_Log.debug( 'Worker abolish delete error! [PostService.py:PostService:abolishworker] --> %s' %e )
        except EnvironmentError as e:
            # socket二次关闭，输出DEBUG日志
            globals.G_Log.debug( 'Worker abolish EnvironmentError! [PostService.py:PostService:abolishworker] --> %s' %e )
        except AttributeError as e:
            # socket被关闭后无法读写，输出DEBUG日志
            globals.G_Log.debug( 'Worker abolish AttributeError! [PostService.py:PostService:abolishworker] --> %s' %e )
        except Exception as e:
            globals.G_Log.error( 'Worker abolish error! [PostService.py:PostService:abolishworker] --> %s' %e )


    def ctosrun(self, worker):
        '''循环读取客户端数据发送给应用
        '''

        globals.G_Log.debug('ctosrun! [PostService.py:PostService:ctosrun]')
        try:
            while True:
                buffer = worker._HC_App_Socket.recv(globals.G_SOCKET_RECV_MAXSIZE)
                if not buffer:
                    globals.G_Log.info( 'client socket close. [PostService.py:PostService:ctosrun]')
                    break
                worker._HttpProxy_HC_Socket.sendall( buffer )
        except AttributeError as e:
            # socket被关闭后无法读写，输出DEBUG日志
            globals.G_Log.debug( 'data post for client to server TypeError! [PostService.py:PostService:ctosrun] --> %s' %e )
        except socket.error as e:
            if e.errno == 10054 or e.errno == 10053 or e.errno == 10058:
                # socket主动关闭的情况下，输出DEBUG日志
                globals.G_Log.debug( 'data post for client to server socket is close! [PostService.py:PostService:ctosrun] --> %s' %e )
            else:
                globals.G_Log.error( 'data post for client to server socket.error! [PostService.py:PostService:ctosrun] --> %s' %e )
        except Exception as e:
            globals.G_Log.error( 'data post for client to server error! [PostService.py:PostService:ctosrun] --> %s' %e )
        finally:
            self.abolishworker(worker)


    def stocrun(self, worker):
        '''循环读取应用数据发送到客户端
        '''

        globals.G_Log.debug('stocrun! [PostService.py:PostService:stocrun]')
        try:
            while True:
                buffer = worker._HttpProxy_HC_Socket.recv(globals.G_SOCKET_RECV_MAXSIZE)
                if not buffer:
                    globals.G_Log.info( 'server socket close. [PostService.py:PostService:stocrun]')
                    break
                worker._HC_App_Socket.sendall( buffer )
        except AttributeError as e:
            # socket被关闭后无法读写，输出DEBUG日志
            globals.G_Log.debug( 'data post for server to client TypeError! [PostService.py:PostService:stocrun] --> %s' %e )
        except socket.error as e:
            if e.errno == 10054 or e.errno == 10053 or e.errno == 10058:
                # socket主动关闭的情况下，输出DEBUG日志
                globals.G_Log.debug( 'data post for server to client socket is close! [PostService.py:PostService:stocrun] --> %s' %e )
            else:
                globals.G_Log.error( 'data post for server to client socket.error! [PostService.py:PostService:stocrun] --> %s' %e )
        except Exception as e:
            globals.G_Log.error( 'data post for server to client error! [PostService.py:PostService:stocrun] --> %s' %e )
        finally:
            self.abolishworker(worker)


    def worksmanager( self, oper, worker ):
        '''proxyworks add and del.
        oper: add or del'''

        globals.G_Log.debug('worksmanager! [PostService.py:PostService:worksmanager]')
        # 返回值，当前work总数
        ret = 0
        # thread lock
        self._HCWorkThreadRLock.acquire()
        try:
            if( oper == 'add' ):
                if ((worker in self._HCWorks) == False):
                    self._HCWorks.append( worker )
            elif( oper == 'del' ):
                if ((worker in self._HCWorks) == True):
                    self._HCWorks.remove( worker )
            ret = len( self._HCWorks )
        except Exception as e:
            globals.G_Log.error( '_HCWorks add or del error! [PostService.py:PostService:worksmanager] --> %s' %e )
        # thread unlock
        self._HCWorkThreadRLock.release()
        # 返回当前work总数
        return ret;
