
def filter_by_currency(transactions, currency):
    '''Функция принимает на вход список словарей, представляющих транзакции.
    Возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной'''
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions):
    '''Генератор принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди'''
    for transaction in transactions:
         yield transaction["description"]

def card_number_generator(start_num:str, end_num:str):
    '''Генератор выдает номера банковских карт в специальном формате,
    принимает начальное и конечное значения для генерации диапазона номеров'''
    start_num_str = str(start_num)
    end_num_str = str(end_num)

    if not start_num_str.isdigit() or not end_num_str.isdigit():
        raise ValueError("Некорректные данные")

    start_num_d = int(start_num)
    end_num_d = int(end_num)
    if start_num_d > end_num_d:
        raise ValueError("Начальный номер не может быть больше конечного")
    list_card_number = []
    for num in range(start_num_d, end_num_d + 1):
        card_num = f"{num:016d}"
        card_num_format = f"{card_num[0:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"
        list_card_number.append(card_num_format)
    return list_card_number
