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

    def __init__(self, count, player_id):
        self.winner = []
        self.deck = []
        self.dealer_hand = []
        self.player_hand = []
        self.dealer_score = [0, 0]
        self.player_score = [0, 0]
        self.done = False
        self.player_id = player_id
        self.deck = game_gen(count)
        self.count = count

    def __del__(self):
        print("Destructor called")
        print(f"killing {id(self)}")

    def win_blackjack(self):
        print('blackjack_check')
        players = [self.player_score, self.dealer_score]
        for player in players:
            if player[0] == 21 or player[1] == 21:
                print(f'checking {player[0], player[1]}')
                if player == self.player_score:
                    self.winner = ['Player', 'Player Blackjack']
                else:
                    self.winner = ['Dealer', 'Dealer Blackjack']

    def win_bust(self):
        print('bust_check')
        players = [self.player_score, self.dealer_score]
        for player in players:
            if player[0] > 21 and player[1] > 21:
                if player == self.player_score:
                    self.winner = ['Dealer', 'Player Bust']
                else:
                    self.winner = ['Player', 'Dealer Bust']

    def win_push(self):
        players = [self.player_score, self.dealer_score]
        print('push_check')
        if (players[0][0] == players[1][0] ) or (players[0][1] == players[1][1]):
            print('push')
            self.winner = ['Draw', 'Push']

    def win_highest(self):
        players = [self.player_score, self.dealer_score]
        print('highest_check')
        if (players[0][0] < players[1][0] and players[1][0] < 21) and (players[1][0] < 21 or players[1][1] < 21):
            self.winner = ['Dealer', 'Dealer Wins']
        elif (players[1][0] < players[0][0] and players[0][0] < 21) and (players[0][0] < 21 or players[0][1] < 21):
            self.winner = ['Player', 'Player Wins']
        for player in players:
            if player[0] > 21 and player[1] > 21:
                if player == self.player_score:
                    self.winner = ['Dealer', 'Player Bust']
                else:
                    self.winner = ['Player', 'Dealer Bust']

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
        self.win_check()

    def win_check(self):
        if len(self.winner) == 2:
            print('winner called')
            print(f"{self.dealer_hand},{self.player_hand}")
            print(self.winner)
            print(id(self))
            del gamelist[str(self.player_id)]
            del self
        elif self.done == True:
            self.win_push()
            self.win_blackjack()
            self.win_bust()
            self.win_highest()
        else:
            self.win_blackjack()
            self.win_bust()

    def deal(self):
        random.shuffle(self.deck)
        for _ in range(2):
            self.draw_player()
            self.draw_dealer()

    def draw_dealer(self):
        self.draw(self.dealer_hand, 'dealer', self.dealer_score)
        self.win_check()

    def draw_player(self):
        self.draw(self.player_hand, 'player', self.player_score)
        self.win_check()

    def hit(self):
        self.draw_player()
        self.win_check()

    def stay(self):
        self.done = True
        while self.dealer_score[1] <= 16:
            self.draw_dealer()
        self.win_highest()
        self.win_check()


    def start(self):
        for _ in range(2):
            self.draw_player()
            self.draw_dealer()
