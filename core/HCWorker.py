#! C:\Python\Python2\python
# -*-coding: utf-8-*-
# FileName: HCWorker.py

# std
# import queue

# org

__all__ = ['HCWorker']

class HCWorker():
    '''HttpConnect构造体，
    持有
      HttpConnect socket(HTTP代理端，应用端两个)
      线程描述符： 读取本地请求 - 发送至远端服务器 
      线程描述符： 读取远端服务器 - 回复至本地 
    '''

    _HttpProxy_HC_Socket = None
    _HC_App_Socket = None
    _CToSThread = None
    _StoCThread = None
    _IsEnable = False
    _Connect_Request = None
    # Connect连接成功
    _IsConnect = False
