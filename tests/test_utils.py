from unittest.mock import patch, mock_open
import pytest
import json

from utils import load_json_data


def test_load_empty_file():
    """Проверяет обработку пустого файла и вывод сообщения
    Мокает os.path.getsize для эмуляции пустого файла"""
    with patch("os.path.getsize", return_value=0):
        result = load_json_data("any_path.json")
        assert result == []


def test_load_non_list_data():
    """Проверяет обработку файла, где JSON не является списком
    Мокает open чтобы избежать открытия файла
    Мокает json.load для возврата словаря (Не списка)"""
    test_data = {"key": "value"}  # Не список
    with patch("builtins.open", mock_open()), patch("json.load", return_value=test_data):
        result = load_json_data("any_path.json")
        assert result == []


def test_load_valid_list_data():
    """Проверяет корректную загрузку валидного JSON-списка
    Мокает open для возврата тестового списка
    Мокает json.load для возврата тестового списка"""
    test_data = [{"id": 1}, {"id": 2}]  # Корректный список
    file_path = "any_path.json"
    with (
        patch("os.path.getsize", return_value=100), # Мок getsize, чтобы файл "существовал" и не был пустым
        patch("builtins.open", mock_open()), # Мок файла
        patch("json.load", return_value=test_data), # Мок json.load
    ):
        result = load_json_data(file_path)
        assert result == test_data


def test_load_invalid_json():
    """Проверяет обработку файла с битым JSON
    Мокает json.load() для эмуляции ошибки декодирования"""
    with patch("builtins.open", mock_open()), patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)):
        result = load_json_data("any_path.json")
        assert result == []


def test_load_nonexistent_file():
    """Проверяет обработку несуществующего файла"""
    non_existent_path = "non_existent_file.json"
    result = load_json_data(non_existent_path)
    assert result == []
