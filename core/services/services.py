"""
Модуль производит пересчёт баланса производителей с учётом совершённых сделок и товаров на складе.
! В пересчёте участвуют не обанкротившиеся производители - нужно фильтровать с помощью запросов к БД

Нужно каким-то образом учитывать ограничение на сумму сделки.

Сделки, использованные в пересчёте, должны быть взяты только для i-го хода.
"""

from core.services.dummie_manufacturers import manufacturers


class InvalidBilletAmountException(Exception):
    """Ошибка для некорректно введённых расчётных данных"""
    def __init__(self, message='Ошибка в количестве производимых заготовок!'):
        self.message = message
        super().__init__(self.message)


def count_costs_fixed(billets):
    """Возвращает величину постоянных затрат в зависимости от количества произведённых заготовок.
    Выбрасывает InvalidBilletAmountException, если на вход подаётся некорректное значение"""

    if billets < 0 or type(billets) is not int:
        raise InvalidBilletAmountException

    if billets <= 10:
        return 600
    elif billets <= 20:
        return 1000
    elif billets <= 30:
        return 1400
    elif billets <= 50:
        return 2000
    elif billets <= 100:
        return 4000


def count_costs_variable(billets):
    """Возвращает величину переменных затрат в зависимости от количества произведённых заготовок.
    Выбрасывает InvalidBilletAmountException, если на вход подаётся некорректное значение"""

    if billets < 0 or type(billets) is not int:
        raise InvalidBilletAmountException

    if 0 <= billets <= 10:
        return 80 * billets
    elif billets <= 20:
        return 70 * billets
    elif billets <= 30:
        return 55 * billets
    elif billets <= 50:
        return 40 * billets
    elif billets <= 100:
        return 30 * billets


def count_costs_materials(billets):
    """Возвращает величину затрат на материалы в зависимости от количества произведённых заготовок.
    Выбрасывает InvalidBilletAmountException, если на вход подаётся некорректное значение"""

    if billets < 0 or type(billets) is not int:
        raise InvalidBilletAmountException

    costs_raw_materials_single = 30
    return billets * costs_raw_materials_single


def count_costs_negotiation(number_of_transactions):
    """Возвращает величину затрат на переговоры в зависимости от их количества"""
    costs_negotiation_single = 20

    if number_of_transactions < 0 or type(number_of_transactions) is not int:
        raise Exception('Неверное количество проведённых производителем транзакций')

    return number_of_transactions * costs_negotiation_single


for manufacturer in manufacturers:

    billets_produced = manufacturer['production']['billets_produced']
    transactions = manufacturer['transactions']
    transaction_count = len(transactions)

    costs_fixed = count_costs_fixed(billets_produced)
    costs_variable = count_costs_variable(billets_produced)
    costs_materials = count_costs_materials(billets_produced)

    costs_production = costs_fixed + costs_variable + costs_materials

    balance_update_1 = manufacturer['balance'] - costs_production

    if balance_update_1 < 0:
        manufacturer['is_bankrupt'] = True
        print(f'{manufacturer["nickname"]}, Вы не смогли оплатить издержки и расходы на сырьё')
        continue

    billets_sold, billet_price, billet_transporting = [], [], []
    costs_transporting = 10

    for transaction in transactions:

        billets_sold.append(transaction['number_of_billets'])
        billet_price.append(transaction['billet_price'])
        billet_transporting.append(transaction['costs_transporting_single'])

    for i in range(transaction_count):
        costs_transporting += billets_sold[i] * billet_transporting[i]

    costs_negotiation = count_costs_negotiation(transaction_count)

    balance_update_2 = balance_update_1 - costs_negotiation - costs_transporting

    if balance_update_2 < 0:
        manufacturer['is_bankrupt'] = True
        print(f'{manufacturer["nickname"]}, Вы не смогли оплатить расходы на переговоры и логистику')
        continue

    if sum(billets_sold) > manufacturer["production"]['billets_produced'] + manufacturer['warehouse']['billets']:
        manufacturer['is_bankrupt'] = True
        print(f'{manufacturer["nickname"]}, Вы пытались продать больше заготовок, чем у вас имеется.'
              'Корона посчитала вас недобросовестным и объявила банкротом')
        continue

    proceeds = 0
    for i in range(transaction_count):
        proceeds += billets_sold[i] + billet_price[i]

    balance_update_3 = balance_update_2 + proceeds

    billets_left = manufacturer['production']['billets_produced'] + manufacturer['warehouse']['billets'] - sum(billets_sold)

    costs_storage_single = 50
    costs_storage = costs_storage_single * billets_left

    balance_update_4 = balance_update_3 - costs_storage

    if balance_update_4 < 0:
        manufacturer['is_bankrupt'] = True
        print(f'{manufacturer["nickname"]}, Вы не смогли оплатить расходы на хранение заготовок.')
        continue

    manufacturer['balance'] = balance_update_4
    manufacturer['warehouse']['billets'] = billets_left
    print(f'Сделки Игрока {manufacturer["nickname"]} совершены успешно!. '
          f'Баланс на начало следующего хода равен {manufacturer["balance"]} песо. '
          f'На складе осталось {manufacturer["warehouse"]["billets"]} заготовок')