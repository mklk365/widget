import pytest
import re
from filtration import process_bank_search


def test_search_transfers(bank_operations):
    """Поиск по слову 'перевод' (должно найти 2 операции)."""
    result = process_bank_search(bank_operations, "перевод")
    assert len(result) == 2
    assert all("Перевод" in op["description"] for op in result)


def test_search_deposits(bank_operations):
    """Поиск по слову 'вклад' (должно найти 2 операции, включая 'Открытие вклада')."""
    result = process_bank_search(bank_operations, "вклад")
    assert len(result) == 2
    assert all("вклад" in op["description"].lower() for op in result)


def test_no_matches(bank_operations):
    """Поиск по отсутствующему слову (например, 'кредит')."""
    result = process_bank_search(bank_operations, "кредит")
    assert len(result) == 0


def test_case_insensitive(bank_operations):
    """Проверка регистронезависимости: 'ОрГаНиЗаЦИи'."""
    result = process_bank_search(bank_operations, "ОрГаНиЗаЦИи")
    assert len(result) == 2
    assert all("организации" in op["description"].lower() for op in result)


def test_empty_data():
    """Пустой список операций на входе."""
    result = process_bank_search([], "перевод")
    assert len(result) == 0


def test_invalid_regex(bank_operations):
    """Некорректное регулярное выражение (например, '*перевод')."""
    result = process_bank_search(bank_operations, "*перевод")
    assert len(result) == 0
