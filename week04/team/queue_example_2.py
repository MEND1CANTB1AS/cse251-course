import threading, queue

def thread_function(q):
    item = q.get()
    print(f'Thread: {item}')

def main():
	q = queue.Queue()

	q.put('one')
	q.put('two')
	q.put('three')

	# Create 3 threads
	# This is a list comprehension
	threads = [threading.Thread(target=thread_function, args=(q, )) for _ in range(3)]

	for i in range(3):
		threads[i].start()

	for i in range(3):
		threads[i].join()

	print('All work completed')

if __name__ == '__main__':
	main()