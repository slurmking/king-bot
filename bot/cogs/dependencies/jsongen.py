import random
import json
cards = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']


def gen_deck():
    deck = []
    for suit in suits:
        for card in cards:
            deck.append(f"{card} of {suit}")
    return deck



value = {'ace': [1,11],
         '2': [2],
         '3': [3],
         '4': [4],
         '5': [5],
         '6': [6],
         '7': [7],
         '8': [8],
         '9': [9],
         '10': [10],
         'Jack': [10],
         'Queen': [10],
         'King': [10]}


list = {}

def search(string):
    for item in value:
        if item in string:
            return value[item]

list = []
dic = {}
for item in gen_deck():
    dic[item]= {'value':search(item),
                'image':'image'}
list.append(dic)
jsonString = json.dumps(list)
print(jsonString)