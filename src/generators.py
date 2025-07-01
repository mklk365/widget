
def filter_by_currency(transactions, currency):
    '''Функция принимает на вход список словарей, представляющих транзакции.
    Возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной'''
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction
        else:
            raise ValueError("Некорректные данные")


def transaction_descriptions():
    '''Генератор принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди'''
    pass

def card_number_generator():
    '''Генератор выдает номера банковских карт в новом формате,
    принимает начальное и конечное значения для генерации диапазона номеров'''
    pass