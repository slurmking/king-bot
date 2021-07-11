import random
import json
import time

gamelist = {}

poop = '1234'
cards = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
with open('bot/cogs/dependencies/deck.json') as f:
    blackjack_json = json.load(f)


def shuffle(deck):
    return random.shuffle(deck)


def gen_deck():
    deck = []
    for suit in suits:
        for card in cards:
            deck.append(f"{card} of {suit}")
    return deck


def game_gen(count):
    hand = []
    for deck in range(count):
        for card in gen_deck():
            hand.append(card)
    random.shuffle(hand)
    return hand


class game:
    winner = []
    deck = []
    dealer_hand = []
    player_hand = []
    dealer_score = [0, 0]
    player_score = [0, 0]
    player_id = 0

    def __del__(self):
        print("object deleted")
    def win_blackjack(self):
        players = [self.player_score, self.dealer_score]
        for player in players:
            if player[0] == 21 or player[1] == 21:
                print(f'checking {player[0], player[1]}')
                if player == self.player_score:
                    self.winner = ['Player', 'Blackjack']
                else:
                    self.winner = ['Dealer', 'Blackjack']

    def win_bust(self):
        players = [self.player_score, self.dealer_score]
        for player in players:
            if player[0] > 21 or player[1] > 21:
                print('bust')
                if player == self.player_score:
                    self.winner = ['Dealer', 'Bust']
                else:
                    self.winner = ['Player', 'Bust']

    def win_push(self):
        players = [self.player_score, self.dealer_score]
        if players[0][0] == players[1][0]:
            self.winner = ['Draw', 'Push']


    def evaluate(self, card):
        return int((blackjack_json[0][card]['value'])[0])

    def evaluate_hand(self, hand, player, score):
        high = 0
        low = 0
        for card in hand:
            if 'ace' in card:
                high += 11
                low += 1
            else:
                high += self.evaluate(card)
                low += self.evaluate(card)
        if player == 'dealer':
            self.dealer_score = [high, low]
        elif player == 'player':
            self.player_score = [high, low]

    def draw(self, hand, player, score):
        card = self.deck[0]
        self.deck.pop(0)
        hand.append(card)
        self.evaluate_hand(hand, player, score)

    def win_check(self):
        self.win_blackjack()
        self.win_bust()
        if self.winner:
            print('delete')
            del gamelist[str(self.player_id)]
            self.__del__()

    def draw_dealer(self):
        self.draw(self.dealer_hand, 'dealer', self.dealer_score)
        self.win_check()
        self.__del__()

    def draw_player(self):
        self.draw(self.player_hand, 'player', self.player_score)
        self.win_check()

    def hit(self):
        self.draw_player()

    def stay(self):
        while self.dealer_score[1] <= 16:
            self.draw_dealer()

    def __init__(self, count,player_id):
        self.player_id = player_id
        self.deck = game_gen(count)
        random.shuffle(self.deck)
        for _ in range(2):
            self.draw_player()
            self.draw_dealer()

