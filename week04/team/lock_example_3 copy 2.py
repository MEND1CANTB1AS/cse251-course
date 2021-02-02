import threading

def thread_function(thread_id, lock, data):
    for i in range(10000000):
        data[thread_id] += 1

def main():    
    lock = threading.Lock()

    # Create a value with each thread
    data = [0] * 3

    # Create 3 threads, pass a "thread_id" for each thread
    threads = [threading.Thread(target=thread_function, args=(i, lock, data)) for i in range(3)]

    for i in range(3):
        threads[i].start()

    for i in range(3):
        threads[i].join()

    print(f'All work completed: {sum(data)}')

if __name__ == '__main__':
    main()