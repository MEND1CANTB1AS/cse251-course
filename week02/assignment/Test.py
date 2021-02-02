import threading

class Add_Two(threading.Thread):

    # constructor
    def __init__(self, number):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.number = number
    
    # This is the method that is run when start() is called
    def run(self):
    	# Create a new variable to hold the answer/results
    	# This variable is public and can be used in the
    	# main function.
    	self.results = self.number + 2
   

if __name__ == '__main__':
	add1 = Add_Two(100)
	add2 = Add_Two(200)

	add1.start()
	add2.start()

	add1.join()
	add2.join()

	print(f'Add_Two(100) returns {add1.results}')
	print(f'Add_Two(200) returns {add2.results}')