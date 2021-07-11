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


def payout(results, bet):
    if results['Queen'] == 3:
        return bet * 200
    elif results['Queen'] == 2:
        return bet * 0
    elif results['Bee3'] == 2:
        return bet * 8
    elif results['Bee3'] == 2:
        return bet * 4
    elif results['Bee2'] == 2:
        return bet * 3
    elif results['Bee1'] == 2:
        return bet * 2
    elif results['Honey'] == 1:
        return bet * 0
    elif results['Honey'] == 2:
        return int(round(bet * 1.5))

    elif results['Honey'] == 3:
        return bet * 2
    elif results['Bee1'] == 3:
        return bet * 4
    elif results['Bee2'] == 3:
        return bet * 6


def slot_spin(bet):
    results_list = {'Queen': 0,
                    'Bee3': 0,
                    'Bee2': 0,
                    'Bee1': 0,
                    'Honey': 0,
                    }
    reel1 = slots()
    reel2 = slots()
    reel3 = slots()
    results_list[f"{reel1.spin()}"] += 1
    results_list[f"{reel2.spin()}"] += 1
    results_list[f"{reel3.spin()}"] += 1
    if reel2.spin() == reel1.spin():
        if reel2.spin() == reel3.spin():
            output = payout(results_list, bet)
        else:
            output = payout(results_list, bet)
    elif results_list['Honey'] >= 1:
        output = payout(results_list, bet)
    else:
        output = 0
    return {'results': results_list,
            'payout': output,
            'reel1': str(reel1.spin()),
            'reel2': str(reel2.spin()),
            'reel3': str(reel3.spin())}
