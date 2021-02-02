import threading

def thread_function(lock, data):
    for i in range(10000000):
        with lock:          # protect the data
            data[0] += 1
        
def main():    
    lock = threading.Lock()

    data = [0]

    # Create 3 threads
    threads = [threading.Thread(target=thread_function, args=(lock, data)) for _ in range(3)]

    for i in range(3):
        threads[i].start()

    for i in range(3):
        threads[i].join()

    print(f'All work completed: {data}')

if __name__ == '__main__':
    main()