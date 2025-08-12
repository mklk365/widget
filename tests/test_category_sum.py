import pytest
from category_sum import process_bank_operations

def test_normal_case(bank_operations):
    """Тест базового сценария"""
    categories = ["Перевод", "Открытие вклада"]
    expected = {"Перевод": 2, "Открытие вклада": 1}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_case_insensitive(bank_operations):
    """Регистронезависимость"""
    categories = ["перевод", "оТКРЫТИЕ"]
    expected = {"перевод": 2, "оТКРЫТИЕ": 1}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_empty_categories(bank_operations):
    """Пустые категории"""
    result = process_bank_operations(bank_operations, [])
    assert result == {}


def test_normal_case(self, bank_operations):
    """Тест нормального случая с несколькими категориями"""
    categories = ["Перевод", "Открытие вклада"]
    expected = {"Перевод": 2, "Открытие вклада": 1}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_case_insensitive(self, bank_operations):
    """Тест регистронезависимости"""
    categories = ["перевод", "оТКРЫТИЕ"]
    expected = {"перевод": 2, "оТКРЫТИЕ": 1}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_empty_categories(self, bank_operations):
    """Тест с пустым списком категорий"""
    result = process_bank_operations(bank_operations, [])
    assert result == {}

def test_no_matching_categories(self, bank_operations):
    """Тест когда нет совпадений с категориями"""
    categories = ["Покупка", "Оплата"]
    expected = {"Покупка": 0, "Оплата": 0}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_partial_matching(self, bank_operations):
    """Тест частичного совпадения в описании"""
    categories = ["организации", "вклад"]
    expected = {"организации": 2, "вклад": 1}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_special_regex_chars_in_categories(self, bank_operations):
    """Тест с категориями содержащими спецсимволы regex"""
    categories = ["Перевод.*", "[О]ткрытие"]
    expected = {"Перевод.*": 0, "[О]ткрытие": 1}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected
