import threading
import Queue
import time 
import multiprocessing

def stringFunction(value, out_queue):
    my_str = "This is string no. " + str(value)
    out_queue.put(my_str)

my_queue = Queue.Queue()

for i in range(20):
    thread1 = threading.Thread(target=stringFunction, args=[i, my_queue])
    thread1.start()

thread1.join()


while not my_queue.empty():
    print(my_queue.get())
    time.sleep(1)
