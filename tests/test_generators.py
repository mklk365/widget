import pytest
from src.generators import filter_by_currency,transaction_descriptions, card_number_generator

@pytest.mark.parametrize("value, code, expected", [
    # Фильтрация по USD
    ([
        {
            "id": 939719570,
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            },
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 873106923,
            "operationAmount": {
                "currency": {
                    "code": "RUB"
                }
            },
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ],
    "USD",
    [
        {
            "id": 939719570,
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            },
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        }
    ]),
    # Фильтрация по RUB
    ([
        {
            "id": 939719570,
            "operationAmount": {
                "currency": {
                    "code": "USD"
                }
            },
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 873106923,
            "operationAmount": {
                "currency": {
                    "code": "RUB"
                }
            },
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ],
    "RUB",
    [
        {
            "id": 873106923,
            "operationAmount": {
                "currency": {
                    "code": "RUB"
                }
            },
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]),
    # Фильтрация если пустой список
    ([], "RUB", [])
])
def test_filter_by_currency(value, code, expected):
    assert list(filter_by_currency(value, code)) == expected

def test_transaction_descriptions(list_tranzact_test):
    gen = transaction_descriptions(list_tranzact_test)
    assert next(gen) == "Перевод организации"

def test_card_number_generator():
    pass