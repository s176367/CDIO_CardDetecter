#!/usr/bin/env python

import random
import socket
import json
from json import JSONEncoder

HOST = "localhost"
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


""" class CardPile:
  def __init__(self, cardPile):
    self.cardPile = cardPile
 """
 
class Card:
  def __init__(self, value, suit):
    self.value = value
    self.suit = suit
    

class CardPileEncoder(JSONEncoder):
  def default(self, o):
    return o.__dict__

deckpile = []


def whileReact(deckpile):


  data = sock.recv(1024).decode("utf-8")
  if data.__contains__("singleCard"):
    for i in deckpile:
      singleCard = i
      deckpile.remove(i)
      break

    sendMig = singleCard
    CardPileJson = json.dumps(sendMig, indent=0,  cls=CardPileEncoder)
    sock.sendall((CardPileJson + "\n").encode("utf-8"))
    print("card sended")

  if data.__contains__("startDeck"):
    cardPile = []
    counter = 0
    for i in deckpile:
      cardPile.append(i)
      counter = counter +1
      if counter > 6:
        break
    for i in deckpile:
      deckpile.remove(i)
      counter = counter +1
      if counter > 6:
        break

      
    sendMig = cardPile
    CardPileJson = json.dumps(sendMig, indent=0,  cls=CardPileEncoder)
    sock.sendall((CardPileJson + "\n").encode("utf-8"))
    print(CardPileJson)


  

#data = sock.recv(1024).decode("uft-8")
#print(data)