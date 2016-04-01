#! C:\Python\Python3\python
# -*- coding: utf-8 -*-
# FileName: queue_test.py

# STD
import queue


if __name__ == '__main__' :
    myQueue = queue.Queue(2)
    myQueue.put('hello world!')

    while (myQueue.empty() != True):
        strstr = myQueue.get()
        if strstr is None:
            break
        print (strstr)
        myQueue.task_done()