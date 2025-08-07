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
