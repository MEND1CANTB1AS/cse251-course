import threading, queue

q = queue.Queue()

q.put('House')
q.put('tree')
q.put('Farm')
q.put('Truck')

print(f'Size of queue = {q.qsize()}')
print(q.get())

print(f'Size of queue = {q.qsize()}')
print(q.get())