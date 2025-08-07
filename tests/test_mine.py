import pytest
from unittest.mock import patch, mock_open

from mine import format_transaction, mine, process_transactions

"""Тестирование mine"""


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            ["1", "EXECUTED", "нет", "нет", "нет"],
            {"file_type": "1", "status": "EXECUTED", "sort_by_date": False, "rub_only": False, "filter_by_word": False},
        ),
        (
            ["2", "CANCELED", "да", "по возрастанию", "да", "да", "перевод"],
            {
                "file_type": "2",
                "status": "CANCELED",
                "sort_by_date": True,
                "sort_by_date_up": True,
                "rub_only": True,
                "filter_by_word": True,
                "filter_word": "перевод",
            },
        ),
    ],
)
def test_mine(inputs, expected):
    """Тестирует mine() с разными входными данными"""
    with patch("builtins.input", side_effect=inputs):
        result = mine()
        assert result == expected


def test_mine_invalid_file_type():
    """Тестирует обработку некорректного типа файла в mine()"""
    with patch("builtins.input", return_value="4"):
        assert mine() is None


"""Тестирование process_transactions"""

TEST_JSON = """[
    {"state": "EXECUTED", "date": "2023-01-01", "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}},
    {"state": "CANCELED", "date": "2023-01-02", "operationAmount": {"amount": "200", "currency": {"code": "USD"}}}
]"""

TEST_CSV = """state;date;operationAmount
EXECUTED;2023-01-01;{"amount": "100", "currency": {"code": "RUB"}}
CANCELED;2023-01-02;{"amount": "200", "currency": {"code": "USD"}}
"""


@pytest.mark.parametrize("file_type,expected_count", [("1", 1), ("2", 1)])  # JSON - только EXECUTED  # CSV - только EXECUTED
def test_process_transactions(file_type, expected_count):
    """Тестирует фильтрацию транзакций по статусу для разных типов файлов"""
    params = {"file_type": file_type, "status": "EXECUTED", "sort_by_date": False, "rub_only": False, "filter_by_word": False}

    mock_data = TEST_JSON if file_type == "1" else TEST_CSV
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = process_transactions(params, "dummy_path")
        assert len(result) == expected_count
        assert all(t["state"] == "EXECUTED" for t in result)


def test_process_empty_file():
    """Тестирует обработку пустого файла"""
    params = {"file_type": "1", "status": "EXECUTED"}
    with patch("builtins.open", mock_open(read_data="[]")):
        assert process_transactions(params, "empty.json") == []


"""Тестирование format_transaction"""


def test_format_transaction_card_to_account():
    """Тестирует форматирование перевода с карты на счет"""
    transaction = {
        "date": "2023-01-01T00:00:00",
        "description": "Перевод",
        "from": "Visa 1234567890123456",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "1000.50", "currency": {"name": "руб."}},
    }

    with (
        patch("masks.get_mask_card_number", return_value="1234 56** **** 3456"),
        patch("masks.get_mask_account", return_value="**7890"),
    ):
        result = format_transaction(transaction)
        assert "01.01.2023 Перевод" in result
        assert "Visa 1234 56** **** 3456 -> Счет **7890" in result
        assert "Сумма: 1000.5 руб." in result


def test_format_deposit():
    """Тестирует форматирование операции открытия вклада"""
    transaction = {
        "date": "2023-01-01T00:00:00",
        "description": "Открытие вклада",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "1000", "currency": {"name": "USD"}},
    }

    with patch("masks.get_mask_account", return_value="**7890"):
        result = format_transaction(transaction)
        assert "Счет **7890" in result
        assert "->" not in result
