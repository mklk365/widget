import json
import csv
import os
import logging
import pandas as pd


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_file_path = os.path.join(PROJECT_ROOT, "data", "operations.json")
csv_file_path = os.path.join(PROJECT_ROOT, "data", "transactions.csv")
xlsx_file_path = os.path.join(PROJECT_ROOT, "data", "transactions_excel.xlsx")

# Путь к папке logs
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")  # Путь к корневой папке logs
LOG_FILE = os.path.join(LOG_DIR, "utils_logger.log")  # Полный путь к файлу лога
os.makedirs(LOG_DIR, exist_ok=True)  # Создаем папку logs, если её нет

# Настройка логгера (перед использованием в функциях)
utils_logger = logging.getLogger(__name__)  # Создание и получение именованного логера
utils_logger.setLevel(logging.DEBUG)  # Настройка уровня логгирования
utils_logger.handlers = []  # Очистка старых обработчиков
# Создаем хендлер для вывода в файл
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")  # Новый лог при каждом запуске
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)

# Принудительно пишем тестовое сообщение
utils_logger.info("Логгер инициализирован!")


def load_json_data(json_file_path):
    """Функция принимает JSON-файл и возвращает список словарей
    с данными о финансовых транзакциях"""
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:  # Считывает JSON
            data = json.load(file)
        if not isinstance(data, list):  # Проверка типа данных
            utils_logger.warning("Данные не являются списком!")
            return []
        return data
    except FileNotFoundError:
        utils_logger.error(f"Файл '{json_file_path}' не найден!")
        return []
    except json.JSONDecodeError:  # Ошибка формата JSON
        utils_logger.error("Invalid JSON data")
        return []


def load_csv_data(csv_file_path):
    """Функция принимает CSV-файл и возвращает список словарей
    с данными о финансовых транзакциях"""
    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            data = list(reader)  # Преобразуем в список
            if not data:  # Проверка на пустые данные
                utils_logger.warning("Пустые данные!")
                return []
            return data
    except FileNotFoundError:
        utils_logger.error(f"Файл '{csv_file_path}' не найден!")
        return []
    except UnicodeDecodeError as e:
        utils_logger.error(f"Ошибка кодировки файла: {e}")
        return []
    except csv.Error as e:
        utils_logger.error(f"Ошибка формата CSV: {e}")
        return []


def load_xlsx_data(xlsx_file_path):
    """Функция принимает XLSX-файл и возвращает список словарей
    с данными о финансовых транзакциях"""
    try:
        with open(xlsx_file_path, "rb") as file:
            df = pd.read_excel(file)
            data = df.to_dict("records")  # Для получения списка словарей
            if not data:  # Проверка на пустые данные
                utils_logger.warning("Пустые данные!")
                return []
            return data
    except FileNotFoundError:
        utils_logger.error(f"Файл '{xlsx_file_path}' не найден!")
        return []
    except Exception as e:  # Исключение для ошибок pandas
        utils_logger.error(f"Ошибка при чтении XLSX файла: {e}")
        return []


# if __name__ == "__main__":
#     data = load_json_data(file_path)
#     if data:
#         print("Данные загружены успешно!")
#     else:
#         print("Не удалось загрузить данные.")
