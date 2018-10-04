import threading
import Queue
import time 
import multiprocessing

def get_page(q):
    
    q.put(my_str)

my_queue = Queue.Queue()

for i in range(20):
    thread1 = threading.Thread(target=stringFunction, args=[i, my_queue])
    thread1.start()

thread1.join()

while not my_queue.empty():
    print(my_queue.get())
    time.sleep(1)
