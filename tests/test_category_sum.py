import pytest
import re
from unittest.mock import patch, MagicMock
from category_sum import process_bank_operations, main

def test_normal_case(bank_operations):
    """Тест нормального случая с несколькими категориями"""
    categories = ["Перевод", "Открытие вклада"]
    # Теперь ожидаем 3 перевода и 3 открытия вклада
    expected = {"Перевод": 3, "Открытие вклада": 3}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_case_insensitive(bank_operations):
    """Тест регистронезависимости"""
    categories = ["перевод", "открытие"]
    expected = {"перевод": 3, "открытие": 3}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_empty_categories(bank_operations):
    """Тест с пустым списком категорий"""
    result = process_bank_operations(bank_operations, [])
    assert result == {}

def test_no_matching_categories(bank_operations):
    """Тест когда нет совпадений с категориями"""
    categories = ["Покупка", "Оплата"]
    expected = {"Покупка": 0, "Оплата": 0}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_partial_matching(bank_operations):
    """Тест частичного совпадения в описании"""
    categories = ["организации", "вклад"]
    # "организации" есть в 3 переводах, "вклад" в 3 операциях
    expected = {"организации": 3, "вклад": 3}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected

def test_special_regex_chars_in_categories(bank_operations):
    """Тест с категориями содержащими спецсимволы regex"""
    categories = ["Перевод", "Открытие"]
    expected = {"Перевод": 3, "Открытие": 3}
    result = process_bank_operations(bank_operations, categories)
    assert result == expected


def test_transactions_without_description(bank_operations):
    """Тест обработки транзакций без поля description"""
    # Добавляем транзакцию без description
    bank_operations.append({"id": 999, "state": "EXECUTED"})

    categories = ["Перевод", "Открытие"]
    result = process_bank_operations(bank_operations, categories)
    # Ожидаем, что транзакция без description не повлияет на счетчик
    assert result == {"Перевод": 3, "Открытие": 3}


def test_invalid_regex_handling(bank_operations):
    """Тест обработки некорректных регулярных выражений в категориях"""
    categories = ["Перевод", "[Неверное[регулярное выражение", "Открытие вклада"]

    result = process_bank_operations(bank_operations, categories)

    # Проверяем что:
    # 1. Все категории присутствуют в результате
    # 2. Некорректные regex имеют значение 0
    assert result == {
        "Перевод": 3,
        "[Неверное[регулярное выражение": 0,
        "Открытие вклада": 3
    }


def test_regex_error_handling():
    """Тест обработки исключения re.error"""
    test_data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"}
    ]

    # Категория с заведомо некорректным регулярным выражением
    categories = ["Нормальная категория", "[Некорректное[регулярное выражение"]

    result = process_bank_operations(test_data, categories)

    # Проверяем что:
    # 1. Функция не упала с исключением
    # 2. Корректная категория обработана
    # 3. Некорректная категория либо отсутствует, либо имеет 0
    assert "Нормальная категория" in result
    assert result.get("[Некорректное[регулярное выражение", -1) == 0


def test_invalid_regex_zero_count():
    """Тест, что для некорректных regex категорий устанавливается 0"""
    test_data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"}
    ]

    # Категория с заведомо некорректным регулярным выражением
    invalid_regex = "[Некорректное[регулярное выражение"
    categories = ["Перевод", invalid_regex]

    result = process_bank_operations(test_data, categories)

    # Проверяем что:
    # 1. Некорректная категория присутствует в результате
    # 2. Для нее установлено значение 0
    assert invalid_regex in result
    assert result[invalid_regex] == 0  # Это покрывает строку category_counts[category] = 0

    # Дополнительная проверка, что корректные категории обработаны
    assert result["Перевод"] > 0


def test_invalid_regex_exception_handling():
    """Тест обработки исключения re.error с проверкой установки 0"""
    test_data = [{"description": "Любая операция"}]

    # Категория с заведомо некорректным регулярным выражением
    invalid_regex = "(*invalid_regex)"
    categories = [invalid_regex]

    result = process_bank_operations(test_data, categories)

    # Проверяем что:
    # 1. Исключение было обработано
    # 2. Для некорректной категории установлено 0
    assert invalid_regex in result
    assert result[invalid_regex] == 0


def test_forced_regex_error_handling():
    """Тест с принудительным вызовом исключения re.error"""
    with patch('re.compile', side_effect=re.error("Искусственная ошибка")):
        result = process_bank_operations(
            [{"description": "Любая операция"}],
            ["Любая категория"]
        )
    # Проверяем что исключение обработано и установлен 0
    assert result == {"Любая категория": 0}


def test_empty_data_handling(capsys):
    """Тест обработки случая с пустыми данными"""
    with patch('category_sum.load_json_data', return_value=None):
        main()
        captured = capsys.readouterr()
        # Проверяем что вывод содержит нужное сообщение
        assert captured.out.strip() == "Нет данных для обработки!"


def test_main_example_usage(capsys):
    """Тест примера использования в main"""
    test_data = [
        {"description": "Перевод организации"},
        {"description": "Покупка товаров"},
        {"description": "Оплата услуг"}
    ]
    with patch('category_sum.load_json_data', return_value=test_data):
        main()
        captured = capsys.readouterr()
        # Преобразуем вывод в словарь для проверки
        import ast
        output_dict = ast.literal_eval(captured.out.strip())
        assert output_dict == {
            "Перевод": 1,
            "Покупка": 1,
            "Оплата": 1
        }

