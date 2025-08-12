import pytest
import re
from filtration import process_bank_search, main


def test_search_transfers(bank_operations):
    """Поиск по слову 'перевод' (должно найти 3 операции)."""
    result = process_bank_search(bank_operations, "перевод")
    assert len(result) == 3


def test_search_deposits(bank_operations):
    """Поиск по слову 'вклад' (должно найти 3 операции)."""
    result = process_bank_search(bank_operations, "вклад")
    assert len(result) == 3


def test_no_matches(bank_operations):
    """Поиск по отсутствующему слову (например, 'кредит')."""
    result = process_bank_search(bank_operations, "кредит")
    assert len(result) == 0


def test_case_insensitive(bank_operations):
    """Проверка регистронезависимости: 'ОрГаНиЗаЦИи'."""
    result = process_bank_search(bank_operations, "ОрГаНиЗаЦИи")
    assert len(result) == 3  # В 3 переводах есть "организации"


def test_empty_data():
    """Пустой список операций на входе."""
    result = process_bank_search([], "перевод")
    assert len(result) == 0


def test_invalid_regex(bank_operations):
    """Некорректное регулярное выражение (например, '*перевод')."""
    result = process_bank_search(bank_operations, "*перевод")
    assert len(result) == 0


def test_main_with_data_successful_search(bank_operations, capsys, monkeypatch):
    """Тест main с данными и успешным поиском"""
    # Мокаем загрузку данных
    monkeypatch.setattr("filtration.load_json_data", lambda _: bank_operations)

    # Вызываем main
    from filtration import main

    main()

    captured = capsys.readouterr()
    assert "Нет данных для обработки!" not in captured.out
    # Проверяем что вывод содержит результат поиска (формат зависит от ваших данных)
    assert "Перевод" in captured.out or "перевод" in captured.out


def test_main_with_empty_data(capsys, monkeypatch):
    """Тест main при отсутствии данных"""
    # Мокаем загрузку пустых данных
    monkeypatch.setattr("filtration.load_json_data", lambda _: [])

    # Вызываем main
    from filtration import main

    main()

    captured = capsys.readouterr()
    assert "Нет данных для обработки!" in captured.out


def test_main_output_format(bank_operations, capsys, monkeypatch):
    """Тест формата вывода результатов"""
    # Мокаем загрузку данных
    monkeypatch.setattr("filtration.load_json_data", lambda _: bank_operations)

    # Вызываем main
    from filtration import main

    main()

    captured = capsys.readouterr()
    # Проверяем что вывод похож на список словарей
    assert captured.out.startswith("[") and captured.out.endswith("]\n")
    # Или более строгая проверка формата, если знаете точный формат вывода


def test_main_file_error_handling(capsys, monkeypatch):
    """Тест обработки ошибок при загрузке файла"""

    # Мокаем функцию load_json_data чтобы она вызывала ошибку
    def mock_load_failed(_):
        raise FileNotFoundError("File not found")

    monkeypatch.setattr("filtration.load_json_data", mock_load_failed)
    main()
    captured = capsys.readouterr()
    assert "Файл с данными не найден!" in captured.out


def test_main_general_exception_handling(capsys, monkeypatch):
    """Тест обработки других исключений"""

    def mock_load_failed(_):
        raise Exception("Some error")

    monkeypatch.setattr("filtration.load_json_data", mock_load_failed)
    main()
    captured = capsys.readouterr()
    assert "Произошла ошибка: Some error" in captured.out


def test_main_successful_execution(bank_operations, capsys, monkeypatch):
    """Тест успешного выполнения"""
    monkeypatch.setattr("filtration.load_json_data", lambda _: bank_operations)

    from filtration import main

    main()

    captured = capsys.readouterr()
    assert "Нет данных для обработки!" not in captured.out
    assert "Файл с данными не найден!" not in captured.out
    assert "Произошла ошибка" not in captured.out
