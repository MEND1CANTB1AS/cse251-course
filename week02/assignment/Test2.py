import threading
import time

class Display_Hello(threading.Thread):

    # constructor
    def __init__(self, number):
        # calling parent class constructor
        threading.Thread.__init__(self)

        # Create or assign any variables that you need
        self.number = number
    
    # This is the method that is run when start() is called
    def run(self):
        time.sleep(self.number)
        print(f'Hello World: {self.number}')
    

if __name__ == '__main__':
	hello1 = Display_Hello(2)
	hello2 = Display_Hello(1)

	hello1.start()
	hello2.start()

	hello1.join()
	hello2.join()