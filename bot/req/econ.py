from req import database


class currency_mismatch(Exception):
    """Raise for my specific kind of exception"""

def format(credit):
    return (f'{credit:,}')

def update(userid, amount):
    current = (database.database_fetch(f'SELECT credit FROM `currency` WHERE user_id = {userid} ')[0])
    total = amount + current
    if current + amount <= 0:
        raise currency_mismatch
        return
    database.database_update(f'UPDATE `currency` SET `credit`={total} WHERE `user_id` = {userid}')
    return current, total

def set(userid,amount):
    database.database_update(f'UPDATE `currency` SET `credit`={amount} WHERE `user_id` = {userid}')
def lookup(userid):
    return database.database_fetch(f'SELECT credit FROM `currency` WHERE user_id = {userid} ')[0]


# print(lookup(260203024431972353))
# print(update('260203024431972353',-50000))
