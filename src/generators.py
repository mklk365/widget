from typing import List, Dict, Any, Generator


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any]]:
    """Функция принимает на вход список словарей, представляющих транзакции.
    Возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной"""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, int]]) -> Generator[Dict[str, Any]]:
    """Генератор принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start_num: str | int, end_num: str | int) -> List[str]:
    """Генератор принимает начальное и конечное значения для генерации диапазона номеров
    и выдает номера банковских карт в специальном формате"""
    start_num_str = str(start_num)
    end_num_str = str(end_num)

    if not start_num_str.isdigit() or not end_num_str.isdigit():
        raise ValueError("Некорректные данные")

    start_num_d = int(start_num)
    end_num_d = int(end_num)

    if start_num_d < 1 or end_num_d < 1:
        raise ValueError("Номера должны быть положительными")

    if end_num_d > 9999999999999999:
        raise ValueError("Конечный номер не может быть больше 9999999999999999")

    if start_num_d > end_num_d:
        raise ValueError("Начальный номер не может быть больше конечного")

    list_card_number = []
    for num in range(start_num_d, end_num_d + 1):
        card_num = f"{num:016d}"
        card_num_format = f"{card_num[0:4]} {card_num[4:8]} {card_num[8:12]} {card_num[12:16]}"
        list_card_number.append(card_num_format)
    return list_card_number
