"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Don't include any other packages/modules.
- Use the website http://deckofcardsapi.com to implement then
  methods below.  Go to this website to get documentation on
  the API calls allowed.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    def __init__(self, url):
        threading.Thread.__init__(self)

        self.url = url

    def run(self):
        response = requests.get(self.url)
        self.response = response.json()    

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        # TODO - add call to reshuffle
        url = f'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/'
        request_thread = Request_thread(url)
        request_thread.start()
        request_thread.join()
        #requests.get(f'https://deckofcardsapi.com/api/deck/{self.deck_id}/shuffle/')

    def draw_card(self):
        # TODO add call to get a card
        url = f'https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=1'
        request_thread = Request_thread(url)
        request_thread.start()
        request_thread.join()
        return request_thread.response.cards(0)
        

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = '2itlbxyzg1gm'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

    # TODO once you have the functions above working, write a card game.
    # (ie., war, 31, UNO, etc...)
    # you can run the program "temp_get_deck_id.py" to get multiple decks
    # if you need them.

    while True:
        print('Press any key to start the game\n')
        input()
        deck = Deck(deck_id)
        user1 = deck.draw_card()
        user2 = deck.draw_card()
        if user1.value > user2:
            print('User 1 Won')
        else if user2.value > user1:
            print('User 2 Won')
        else:
            print('No one won')