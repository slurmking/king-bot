import random
from random import randint


class slots:
    def __init__(self):
        self.number = randint(0, 999)

    def spin(self):
        if 0 <= self.number <= 99:
            return 'Queen'
        elif 100 <= self.number <= 399:
            return 'Honey'
        elif 400 <= self.number <= 699:
            return 'Bee1'
        elif 700 <= self.number <= 899:
            return 'Bee2'
        elif 900 <= self.number <= 999:
            return 'Bee3'

def payout(results,bet):
    if results['Queen'] == 3:
        return bet * 200
    elif results['Honey'] == 2:
        return bet * 2
    elif results['Bee1'] == 2:
        return bet * 4
    elif results['Bee2'] == 2:
        return bet * 6
    elif results['Bee3'] == 2:
        return bet * 8
    elif results['Honey'] == 3:
        return bet * 4
    elif results['Bee1'] == 3:
        return bet * 8
    elif results['Bee2'] == 3:
        return bet * 12
    elif results['Bee3'] == 2:
        return bet * 16
def slotSpin(bet):
    resultsList = {'Queen': 0,
                   'Bee3': 0,
                   'Bee2': 0,
                   'Bee1': 0,
                   'Honey': 0,
                   }
    reel1 = slots()
    reel2 = slots()
    reel3 = slots()
    resultsList[f"{reel1.spin()}"] += 1
    resultsList[f"{reel2.spin()}"] += 1
    resultsList[f"{reel3.spin()}"] += 1
    print(f"{reel1.spin()} - {reel2.spin()} - {reel3.spin()}")
    print(resultsList)
    print (payout(resultsList,bet))

slotSpin(13)

