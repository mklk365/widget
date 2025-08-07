from unittest.mock import patch, mock_open
import json
import csv
import pandas as pd

from utils import load_json_data, load_csv_data, load_xlsx_data
import logging

# 1. Тесты load_json_data


def test_load_empty_json():
    """Проверяет обработку пустого файла и вывод сообщения
    Мокает os.path.getsize для эмуляции пустого файла"""
    with patch("os.path.getsize", return_value=0):
        result = load_json_data("any_path.json")
        assert result == []


def test_load_non_list_json():
    """Проверяет обработку файла, где JSON не является списком
    Мокает open чтобы избежать открытия файла
    Мокает json.load для возврата словаря (Не списка)"""
    test_data = {"key": "value"}  # Не список
    with patch("builtins.open", mock_open()), patch("json.load", return_value=test_data):
        result = load_json_data("any_path.json")
        assert result == []


def test_load_valid_list_json():
    """Проверяет корректную загрузку валидного JSON-списка
    Мокает open для возврата тестового списка
    Мокает json.load для возврата тестового списка"""
    test_data = [{"id": 1}, {"id": 2}]  # Корректный список
    file_path = "any_path.json"
    with (
        patch("os.path.getsize", return_value=100),  # Мок getsize, чтобы файл "существовал" и не был пустым
        patch("builtins.open", mock_open()),  # Мок файла
        patch("json.load", return_value=test_data),  # Мок json.load
    ):
        result = load_json_data(file_path)
        assert result == test_data


def test_load_invalid_json():
    """Проверяет обработку файла с битым JSON
    Мокает json.load() для эмуляции ошибки декодирования"""
    with patch("builtins.open", mock_open()), patch("json.load", side_effect=json.JSONDecodeError("Error", "doc", 0)):
        result = load_json_data("any_path.json")
        assert result == []


def test_load_nonexistent_json():
    """Пайл json не существует"""
    non_existent_path = "non_existent_file.json"
    result = load_json_data(non_existent_path)
    assert result == []  # Ожидается пустой список


# 2. Тесты load_csv_data


def test_load_nonexistent_csv():
    """Файл csv не существует"""
    non_existent_path = "non_existent_file.csv"
    result = load_csv_data(non_existent_path)
    assert result == []  # Ожидается пустой список


def test_encoding_csv():
    """Проверяет обработку CSV с некорректной кодировкой."""
    with patch("builtins.open") as mocked_open, patch("utils.utils_logger.error") as mocked_logger:
        # Эмулируем ошибку кодировки ПРИ ОТКРЫТИИ файла
        mocked_open.side_effect = UnicodeDecodeError("utf-8", b"\xff\x00", 0, 1, "Invalid UTF-8")
        result = load_csv_data("any_path.csv")
        assert result == []  # Проверяем возвращаемое значение
        # Проверяем, что логгер был вызван с нужной ошибкой
        mocked_logger.assert_called_once()
        assert "Ошибка кодировки файла" in mocked_logger.call_args[0][0]


def test_delimiter_csv():
    """CSV с разделителем ',' не парсится.
    Мокает open и csv.DictReader"""
    csv_content = """id,amount,date
    1,100,2023-01-01"""
    with patch("builtins.open", mock_open(read_data=csv_content)), patch("csv.DictReader") as mock_dict_reader:
        # Эмулируем, что DictReader вернет пустой список (т.к. разделитель не ';')
        mock_dict_reader.return_value = []
        result = load_csv_data("any_path.csv")
        assert result == []  # Ожидается пустой список


def test_empty_csv():
    """Тест для пустых данных"""
    with patch("builtins.open", mock_open(read_data="")):
        result = load_csv_data("empty.csv")
        assert result == []  # Ожидается пустой список


def test_successful_csv():
    """Тест успешного чтения данных"""
    csv_content = "date;amount\n2023-01-01;100\n2023-01-02;200"
    with patch("builtins.open", mock_open(read_data=csv_content)):
        result = load_csv_data("good.csv")
        expected = [{"date": "2023-01-01", "amount": "100"}, {"date": "2023-01-02", "amount": "200"}]
        assert result == expected


def test_parsing_error_csv():
    """Проверяет обработку ошибки парсинга CSV"""
    with patch("builtins.open", mock_open(read_data="invalid;csv;data")), patch("csv.DictReader") as mock_reader:
        mock_reader.side_effect = csv.Error("CSV parsing error")
        result = load_csv_data("bad.csv")  # Вызываем функцию
        assert result == []


# 3. Тесты load_xlsx_data


def test_success_xlsx(tmp_path):
    """Тест успешной загрузки XLSX-файла"""
    # Создаем временный XLSX-файл
    test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    test_df = pd.DataFrame(test_data)
    test_file = tmp_path / "test.xlsx"
    test_df.to_excel(test_file, index=False)
    # Тестируем с реальным файлом
    result = load_xlsx_data(test_file)
    assert result == test_data


def test_empty_xlsx(tmp_path):
    """Тест обработки пустого XLSX-файла"""
    # Создаем временный пустой файл
    test_file = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(test_file, index=False)  # Пустой DataFrame
    # Мокаем read_excel через patch
    with patch("pandas.read_excel", return_value=pd.DataFrame()):
        result = load_xlsx_data(test_file)
    assert result == []  # Ожидается пустой список


def test_not_found_xlsx():
    """Тест обработки случая, когда файл не найден"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_xlsx_data("nonexistent.xlsx")
    assert result == []  # Ожидается пустой список


def test_corrupted_xlsx():
    """Тест битого XLSX-файла"""
    with patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError("File is empty or corrupted")):
        result = load_xlsx_data("corrupted.xlsx")
        assert result == []  # Ожидается пустой список


def test_logging_xlsx(caplog):
    """Тест логгирования ошибок"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with caplog.at_level(logging.ERROR):
            load_xlsx_data("nonexistent.xlsx")
    assert "Файл 'nonexistent.xlsx' не найден!" in caplog.text


def test_general_exception_xlsx(caplog):
    """Тест обработки других исключений при чтении XLSX"""
    test_exception = Exception("Some pandas error")
    # Мокаем open, чтобы он возвращал "файл", а затем мокаем read_excel, чтобы он падал с ошибкой
    with patch("builtins.open", mock_open()) as mocked_open:
        with patch("pandas.read_excel", side_effect=test_exception):
            with caplog.at_level(logging.ERROR):
                result = load_xlsx_data("test.xlsx")
    assert result == []  # Ожидается пустой список
    assert f"Ошибка при чтении XLSX файла: {test_exception}" in caplog.text
