from threading import *

sem_sofa = Semaphore(3)

sem.acquire()
# Do something
sem.release()

person1 : sem_sofa.acquire() -> sem = 2, access
person2 : sem_sofa.acquire() -> sem = 1, access
person3 : sem_sofa.acquire() -> sem = 0, access
person4 : sem_sofa.acquire() -> no access
# person2.release -> sem 1