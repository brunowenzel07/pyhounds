# -*- coding: UTF-8
# !/usr/bin/python 

import _thread
import time

def task(task_name, delay):
    ct = 0
    while ct < 5:
        ct += 1 
        time.sleep(delay)
        print("Thread: %s" % (task_name))

_thread.start_new_thread(task, ("Tarefa 1", 1))
_thread.start_new_thread(task, ("Tarefa 2", 1))


while True:
    pass