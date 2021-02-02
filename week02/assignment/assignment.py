"""
------------------------------------------------------------------------------
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a website

Comments: Creating a thread to call the data for film 6. Then creating a thread for each
category to display the selected imformation. I believe I scored a 4 on this assignment
and I greatly appreciated your help Brother Comeau.

Instructions:

- each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information form the
  website.
- You are limited to about 10,000 calls to the swapi website.  That sounds like
  a lot, but you can reach this limit. If you leave this assignment to the last
  day it's due, you might be locked out of the website and you will have to
  submit what you have at that point.  There are no extensions because you
  reached this server limit. Work ahead and spread working on the assignment
  over multiple days.
- You need to match the output outlined in the dcription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the swapi server. You
  can define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary.  Do NOT have this
dictionary hard coded - use the API call to get this dictionary.  Then you can
use this dictionary to make other API calls for data.

{
   "people": "http://swapi.dev/api/people/", 
   "planets": "http://swapi.dev/api/planets/", 
   "films": "http://swapi.dev/api/films/",
   "species": "http://swapi.dev/api/species/", 
   "vehicles": "http://swapi.dev/api/vehicles/", 
   "starships": "http://swapi.dev/api/starships/"
}

------------------------------------------------------------------------------
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

# Const Values
TOP_API_URL = 'https://swapi.dev/api'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
  def __init__(self, url):
    threading.Thread.__init__(self)
    self.url = url
    self.response = {}

  def run(self):
    response = requests.get(self.url)
    global call_count
    call_count += 1
        # Check the status code to see if the request succeeded.
    if response.status_code == 200:
        self.response = response.json()
        #print(self.response)
        #print('\nHere is the people url:', self.response['people'])
    else:
        print('RESPONSE = ', response.status_code)


# TODO Add any functions you need here
def retrieve_film_6():
  req = Request_thread(rf'http://swapi.dev/api/films/6/')
  req.start()
  req.join()
  return req.response

def display_film(data):
  # req = Request_thread(rf'http://swapi.dev/api/films/6/')
  # req.start()
  # req.join()
  print('Title      : ', data['title'])
  print('Directror  : ', data['director'])
  print('Producer   : ', data['producer'])
  print('Released   : ', data['release_date'])

def display_characters(data):
  threads = []
  names = []
  for url in data['characters']:
    threads.append(Request_thread(url))
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()  
  for thread in threads:
    characters = thread.response
    names.append(characters['name'])
  names.sort()
  print("\nCharacters: " , len(names))
  print(*names, sep = ", ") 
  
def display_planets(data):
  threads = []
  planets = []
  for url in data['planets']:
    threads.append(Request_thread(url))
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()  
  for thread in threads:
    worlds = thread.response
    planets.append(worlds['name'])
  planets.sort()
  print("\nPlanets: " , len(planets))
  print(*planets, sep = ", ") 

def display_starships(data):
  threads = []
  starships = []
  for url in data['starships']:
    threads.append(Request_thread(url))
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()  
  for thread in threads:
    ships = thread.response
    starships.append(ships['name'])
  starships.sort()
  print("\nStarships: " , len(starships))
  print(*starships, sep = ", ") 

def display_vehicles(data):
  threads = []
  vehicles = []
  for url in data['vehicles']:
    threads.append(Request_thread(url))
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()  
  for thread in threads:
    machines = thread.response
    vehicles.append(machines['name'])
  vehicles.sort()
  print("\nVehicles: " , len(vehicles))
  print(*vehicles, sep = ", ") 

def display_species(data):
  threads = []
  species = []
  for url in data['species']:
    threads.append(Request_thread(url))
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()  
  for thread in threads:
    biology = thread.response
    species.append(biology['name'])
  species.sort()
  print("\nStarships: " , len(species))
  print(*species, sep = ", ")
  print("") 



def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from swapi.dev')

    # TODO Retrieve Top API urls
    req = Request_thread(TOP_API_URL)
    req.start()
    req.join()

    # TODO Retireve Details on film 6
    data = retrieve_film_6()

    # TODO Display results
    display_film(data)

    display_characters(data)

    display_planets(data)

    display_starships(data)

    display_vehicles(data)

    display_species(data)

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')
    

if __name__ == "__main__":
    
    # response = requests.get(TOP_API_URL)
    
    # # Check the status code to see if the request succeeded.
    # if response.status_code == 200:
    #     data = response.json()
    #     print(data)
    #     print(data['films'])
    #     print('\nHere is the people url:', data['people'])
    # else:
    #     print('Error in requesting ID')
    main()
