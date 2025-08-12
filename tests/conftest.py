import pytest
from unittest.mock import patch


@pytest.fixture
def list_date_test():
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def list_tranzact_test():
    return [
        {
            "id": 939719570,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации",
            "to": "Счет 11776614605963066702",
        }
    ]


"""Фикстуры для тестирования модуля работы с транзакциями"""


@pytest.fixture
def mock_masks():
    """Фикстура для мокирования функций маскировки"""
    with patch("masks.get_mask_card_number") as mock_card, patch("masks.get_mask_account") as mock_account:
        mock_card.return_value = "0000 00** **** 0000"
        mock_account.return_value = "**0000"
        yield mock_card, mock_account


@pytest.fixture
def sample_transaction():
    """Фикстура с примером стандартной транзакции"""
    return {
        "date": "2023-01-01T00:00:00",
        "description": "Тест",
        "from": "Visa 1111222233334444",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "100", "currency": {"name": "RUB"}},
    }


@pytest.fixture
def bank_operations():
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Открытие вклада",  # Нет поля 'from'
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 587085106,
            "state": "CANCELED",  # Невыполненная операция
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431",
        },
    ]
