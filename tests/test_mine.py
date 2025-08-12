import pytest
from unittest.mock import patch, mock_open
import pandas as pd

from mine import format_transaction, mine, process_transactions
import masks

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


def test_mine_invalid_status_output(capsys):
    """Тестирует вывод сообщения о недоступном статусе операции"""
    # Подготавливаем входные данные: сначала неверный статус, затем верный
    inputs = ["1", "INVALID_STATUS", "EXECUTED", "нет", "нет", "нет"]

    with patch('builtins.input', side_effect=inputs):
        # Вызываем функцию
        result = mine()

        # Получаем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out

        # Проверяем что сообщение выведено
        assert "Статус операции 'INVALID_STATUS' недоступен." in output

        # Проверяем что функция продолжает работу и возвращает результат
        assert result is not None
        assert result["status"] == "EXECUTED"


def test_mine_xlsx_file_output(capsys):
    """Тестирует вывод сообщения о выборе XLSX-файла"""
    # Подготавливаем входные данные: выбираем XLSX (пункт 3), затем корректный статус и остальные параметры
    inputs = ["3", "EXECUTED", "нет", "нет", "нет"]

    with patch('builtins.input', side_effect=inputs):
        # Вызываем функцию
        result = mine()

        # Получаем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out

        # Проверяем что сообщение выведено
        assert "Для обработки выбран XLSX-файл" in output

        # Проверяем что функция вернула правильный тип файла
        assert result["file_type"] == "3"

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


def test_process_transactions_xlsx_file():
    """Тестирует загрузку данных из XLSX-файла"""
    # Подготовка тестовых данных
    test_data = [
        {"state": "EXECUTED", "date": "2023-01-01", "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    ]

    # Параметры для функции
    params = {
        "file_type": "3",  # XLSX
        "status": "EXECUTED",
        "sort_by_date": False,
        "rub_only": False,
        "filter_by_word": False
    }

    # Мокаем именно ту функцию, которая используется для загрузки XLSX
    with patch('utils.load_xlsx_data', return_value=test_data) as mock_load_xlsx:
        result = process_transactions(params, "test.xlsx")

        # Проверяем что функция загрузки была вызвана
        mock_load_xlsx.assert_called_once_with("test.xlsx")

        # Проверяем результат
        assert len(result) == 1
        assert result[0]["state"] == "EXECUTED"


def test_process_transactions_xlsx_file_not_found():
    """Тестирует обработку отсутствия XLSX-файла"""
    params = {
        "file_type": "3",
        "status": "EXECUTED"
    }

    with patch('utils.load_xlsx_data', return_value=None):
        result = process_transactions(params, "nonexistent.xlsx")
        assert result == []


def test_process_transactions_xlsx_file():
    """Тестирует загрузку данных из XLSX-файла"""
    # Подготовка тестовых данных
    test_data = [
        {"state": "EXECUTED", "date": "2023-01-01", "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    ]

    # Параметры для функции
    params = {
        "file_type": "3",  # XLSX
        "status": "EXECUTED",
        "sort_by_date": False,
        "rub_only": False,
        "filter_by_word": False
    }

    # Вариант 1: Используем полный путь к функции
    with patch('mine.load_xlsx_data', return_value=test_data) as mock_load:
        # Переимпортируем модуль, чтобы применить мок
        import importlib
        from mine import process_transactions
        importlib.reload(mine)

        result = process_transactions(params, "test.xlsx")

        # Проверяем вызовы
        print("Actual calls to load_xlsx_data:", mock_load.mock_calls)

        # Проверяем что функция была вызвана
        assert mock_load.called
        assert mock_load.call_count == 1
        mock_load.assert_called_once_with("test.xlsx")

        # Проверяем результат
        assert len(result) == 1
        assert result[0]["state"] == "EXECUTED"

    # Вариант 2: Альтернативный способ с monkeypatch
    def test_xlsx_loading(monkeypatch):
        def mock_load(path):
            return test_data

        monkeypatch.setattr('mine.load_xlsx_data', mock_load)

        result = process_transactions(params, "test.xlsx")
        assert len(result) == 1


def test_process_transactions_xlsx_file():
    """Тестирует загрузку данных из XLSX-файла"""
    # Подготовка тестовых данных
    test_data = [
        {"state": "EXECUTED", "date": "2023-01-01", "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    ]

    # Параметры для функции
    params = {
        "file_type": "3",  # XLSX
        "status": "EXECUTED",
        "sort_by_date": False,
        "rub_only": False,
        "filter_by_word": False
    }

    # Вариант 1: Мокаем функцию в utils
    with patch('utils.load_xlsx_data', return_value=test_data) as mock_load:
        from mine import process_transactions
        result = process_transactions(params, "test.xlsx")

        # Проверяем что функция была вызвана
        assert mock_load.called
        assert "test.xlsx" in mock_load.call_args[0]

        # Проверяем результат
        assert len(result) == 1
        assert result[0]["state"] == "EXECUTED"

    # Вариант 2: Альтернативный способ с mock.patch.object
    from utils import load_xlsx_data
    with patch.object(load_xlsx_data, '__code__', new=lambda x: test_data):
        result = process_transactions(params, "test.xlsx")
        assert len(result) == 1


# def test_process_transactions_xlsx_file_diagnostic():
#     """Диагностический тест для проверки импортов"""
#     from mine import process_transactions
#     import inspect
#
#     # Проверяем откуда импортируется load_xlsx_data
#     print("\nИмпорты в process_transactions:")
#     for name, val in inspect.getmembers(process_transactions):
#         if inspect.isfunction(val):
#             print(f"{name}: {val.__module__}")
#
#     # Проверяем доступность функции в utils
#     import utils
#     print("\nФункции в utils:", dir(utils))


def test_process_transactions_xlsx_file():
    """Тестирует загрузку данных из XLSX-файла"""
    test_data = [
        {"state": "EXECUTED", "date": "2023-01-01", "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    ]

    params = {
        "file_type": "3",
        "status": "EXECUTED",
        "sort_by_date": False,
        "rub_only": False,
        "filter_by_word": False
    }

    # Вариант 1: Мокаем функцию в том месте, где она реально используется
    with patch('mine.load_xlsx_data', return_value=test_data, create=True) as mock_load:
        from mine import process_transactions
        result = process_transactions(params, "test.xlsx")

        if not mock_load.called:
            print("\nФункция load_xlsx_data не была вызвана. Альтернативные пути:")
            print("Попробуем мокать utils.load_xlsx_data")

            with patch('utils.load_xlsx_data', return_value=test_data) as mock_utils_load:
                result = process_transactions(params, "test.xlsx")
                assert mock_utils_load.called
                assert len(result) == 1
        else:
            assert len(result) == 1


def test_process_transactions_invalid_file_type():
    """Тестирует обработку неверного типа файла"""
    params = {
        "file_type": "4",  # Неверный тип
        "status": "EXECUTED"
    }

    result = process_transactions(params)

    # Проверяем что возвращается пустой список
    assert result == []


def test_process_transactions_rub_only():
    """Тестирует фильтрацию только рублевых транзакций"""
    # Подготовка тестовых данных
    test_data = [
        {"state": "EXECUTED", "operationAmount": {"currency": {"code": "RUB"}}},
        {"state": "EXECUTED", "operationAmount": {"currency": {"code": "USD"}}},
        {"state": "EXECUTED", "operationAmount": {"currency": {"code": "EUR"}}},
        {"state": "EXECUTED", "operationAmount": {"currency": {"code": "RUB"}}},
    ]

    # Параметры с включенной фильтрацией по рублям
    params = {
        "file_type": "1",  # JSON
        "status": "EXECUTED",
        "rub_only": True,  # Включена фильтрация по RUB
        "sort_by_date": False,
        "filter_by_word": False
    }

    with patch('mine.load_json_data', return_value=test_data):
        result = process_transactions(params)

        # Проверяем что остались только рублевые транзакции
        assert len(result) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)


def test_process_transactions_not_rub_only():
    """Тестирует отсутствие фильтрации по валюте"""
    # Подготовка тестовых данных
    test_data = [
        {"state": "EXECUTED", "operationAmount": {"currency": {"code": "RUB"}}},
        {"state": "EXECUTED", "operationAmount": {"currency": {"code": "USD"}}},
    ]

    # Параметры без фильтрации по рублям
    params = {
        "file_type": "1",
        "status": "EXECUTED",
        "rub_only": False,  # Фильтрация по RUB выключена
        "sort_by_date": False,
        "filter_by_word": False
    }

    with patch('mine.load_json_data', return_value=test_data):
        result = process_transactions(params)

        # Проверяем что все транзакции остались
        assert len(result) == 2
        assert any(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)
        assert any(t["operationAmount"]["currency"]["code"] == "USD" for t in result)


def test_process_transactions_rub_only_with_missing_data():
    """Тестирует обработку транзакций с отсутствующими данными о валюте"""
    test_data = [
        {"state": "EXECUTED", "operationAmount": {"currency": {"code": "RUB"}}},
        {"state": "EXECUTED"},  # Нет данных о валюте
        {"state": "EXECUTED", "operationAmount": {}},  # Нет currency
        {"state": "EXECUTED", "operationAmount": {"currency": {}}},  # Нет code
    ]

    params = {
        "file_type": "1",
        "status": "EXECUTED",
        "rub_only": True,
        "sort_by_date": False,
        "filter_by_word": False
    }

    with patch('mine.load_json_data', return_value=test_data):
        result = process_transactions(params)

        # Проверяем что осталась только одна рублевая транзакция
        assert len(result) == 1
        assert result[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_process_transactions_filter_by_partial_word():
    """Тестирует фильтрацию по части слова"""
    test_data = [
        {"state": "EXECUTED", "description": "Перевод организации"},
        {"state": "EXECUTED", "description": "Переводной документ"},
        {"state": "EXECUTED", "description": "Организация перевода"},
    ]

    params = {
        "file_type": "1",
        "status": "EXECUTED",
        "filter_by_word": True,
        "filter_word": "перевод",
        "rub_only": False,
        "sort_by_date": False
    }

    with patch('mine.load_json_data', return_value=test_data):
        result = process_transactions(params)
        assert len(result) == 3  # Все содержат "перевод" в разных формах


def test_process_transactions_sort_ascending():
    """Тестирует сортировку по возрастанию даты"""
    test_data = [
        {"state": "EXECUTED", "date": "2023-01-03"},
        {"state": "EXECUTED", "date": "2023-01-01"},
        {"state": "EXECUTED", "date": "2023-01-02"},
    ]

    params = {
        "file_type": "1",
        "status": "EXECUTED",
        "sort_by_date": True,
        "sort_by_date_up": True,  # Сортировка по возрастанию
        "rub_only": False,
        "filter_by_word": False
    }

    with patch('mine.load_json_data', return_value=test_data):
        result = process_transactions(params)

        # Проверяем порядок дат
        dates = [t["date"] for t in result]
        assert dates == ["2023-01-01", "2023-01-02", "2023-01-03"]


def test_process_transactions_sort_descending():
    """Тестирует сортировку по убыванию даты"""
    test_data = [
        {"state": "EXECUTED", "date": "2023-01-01"},
        {"state": "EXECUTED", "date": "2023-01-03"},
        {"state": "EXECUTED", "date": "2023-01-02"},
    ]

    params = {
        "file_type": "1",
        "status": "EXECUTED",
        "sort_by_date": True,
        "sort_by_date_up": False,  # Сортировка по убыванию
        "rub_only": False,
        "filter_by_word": False
    }

    with patch('mine.load_json_data', return_value=test_data):
        result = process_transactions(params)

        # Проверяем порядок дат
        dates = [t["date"] for t in result]
        assert dates == ["2023-01-03", "2023-01-02", "2023-01-01"]


def test_process_transactions_sort_with_missing_dates():
    """Тестирует сортировку при отсутствии дат у некоторых транзакций"""
    test_data = [
        {"state": "EXECUTED", "date": "2023-01-02"},
        {"state": "EXECUTED"},  # Нет даты
        {"state": "EXECUTED", "date": "2023-01-01"},
    ]

    params = {
        "file_type": "1",
        "status": "EXECUTED",
        "sort_by_date": True,
        "sort_by_date_up": True,
        "rub_only": False,
        "filter_by_word": False
    }

    with patch('mine.load_json_data', return_value=test_data):
        result = process_transactions(params)

        # Проверяем что транзакции без даты в конце
        assert result[0]["date"] == "2023-01-01"
        assert result[1]["date"] == "2023-01-02"
        assert "date" not in result[2]


def test_process_transactions_no_sorting():
    """Тестирует отсутствие сортировки при sort_by_date=False"""
    test_data = [
        {"state": "EXECUTED", "date": "2023-01-03"},
        {"state": "EXECUTED", "date": "2023-01-01"},
    ]

    original_order = [t["date"] for t in test_data]

    params = {
        "file_type": "1",
        "status": "EXECUTED",
        "sort_by_date": False,  # Сортировка отключена
        "sort_by_date_up": True,
        "rub_only": False,
        "filter_by_word": False
    }

    with patch('mine.load_json_data', return_value=test_data):
        result = process_transactions(params)

        # Проверяем что порядок не изменился
        assert [t["date"] for t in result] == original_order

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


def test_format_transaction_invalid_date():
    """Тестирует обработку некорректных форматов даты"""
    # Транзакция с некорректным форматом даты
    transaction_bad_format = {
        "date": "2023/01/01",  # Неправильный формат
        "description": "Перевод",
        "from": "Visa 1234567890123456",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "1000.50", "currency": {"name": "руб."}},
    }

    # Транзакция с датой неправильного типа
    transaction_wrong_type = {
        "date": 1234567890,  # Число вместо строки
        "description": "Перевод",
        "from": "Visa 1234567890123456",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "1000.50", "currency": {"name": "руб."}},
    }

    # Транзакция без даты
    transaction_no_date = {
        "description": "Перевод",
        "from": "Visa 1234567890123456",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "1000.50", "currency": {"name": "руб."}},
    }

    with (
        patch("masks.get_mask_card_number", return_value="1234 56** **** 3456"),
        patch("masks.get_mask_account", return_value="**7890"),
    ):
        # Проверяем обработку неправильного формата даты
        result_bad_format = format_transaction(transaction_bad_format)
        assert "Дата неизвестна Перевод" in result_bad_format

        # Проверяем обработку даты неправильного типа
        result_wrong_type = format_transaction(transaction_wrong_type)
        assert "Дата неизвестна Перевод" in result_wrong_type

        # Проверяем обработку отсутствия даты
        result_no_date = format_transaction(transaction_no_date)
        assert "Дата неизвестна Перевод" in result_no_date


def test_format_transaction_account_no_mask():
    """Тестирует обработку счета при ошибке маскировки"""
    transaction = {
        "date": "2023-01-01T00:00:00",  # Добавляем дату
        "description": "Перевод со счета",
        "from": "Счет 123",  # Неправильный номер счета
        "to": "Счет 98765432109876543210",  # Добавляем получателя
        "operationAmount": {"amount": "1000.00", "currency": {"name": "руб."}},
    }

    with patch("masks.get_mask_account", side_effect=ValueError):
        result = format_transaction(transaction)
        # Проверяем что оригинальный номер счета остался в выводе
        assert "Счет 123" in result
        # Проверяем общий формат вывода
        assert "01.01.2023 Перевод со счета" in result
        assert "Сумма: 1000 руб." in result


def test_format_transaction_card_masking(monkeypatch):
    """Альтернативный вариант с monkeypatch"""
    transaction = {
        "to": "Visa Platinum 1234567890123456",
        "description": "Тест"
    }

    def mock_mask(number):
        assert number == "1234567890123456"
        return "1234 56** **** 3456"

    monkeypatch.setattr('masks.get_mask_card_number', mock_mask)

    result = format_transaction(transaction)
    assert "Visa Platinum 1234 56** **** 3456" in result


def test_format_transaction_card_masking_error():
    """Тестирует обработку ошибки при маскировке номера карты"""
    # Транзакция с некорректным номером карты
    transaction = {
        "date": "2023-01-01T00:00:00",
        "description": "Перевод на карту",
        "to": "Visa Platinum 123",  # Неправильный номер карты
        "operationAmount": {"amount": "1000.00", "currency": {"name": "руб."}},
    }

    # Вариант 1: Используем patch.object для конкретного модуля
    with patch.object(masks, 'get_mask_card_number', side_effect=ValueError("Invalid card number")) as mock_mask:
        result = format_transaction(transaction)

        # Проверяем что в результате используется оригинальный номер карты
        assert "Visa Platinum 123" in result
        assert "01.01.2023 Перевод на карту" in result
        assert "Сумма: 1000 руб." in result

    # Вариант 2: Альтернативный способ с переимпортом
    import importlib
    import mine
    importlib.reload(mine)

    with patch('mine.get_mask_card_number', side_effect=ValueError("Invalid card number")) as mock_mask:
        result = mine.format_transaction(transaction)
        assert "Visa Platinum 123" in result