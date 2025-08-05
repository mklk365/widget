import json
import os
import logging


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# путь к JSON
file_path = os.path.join(PROJECT_ROOT, "data", "operations.json")


def load_json_data(file_path):
    """Функция принимает JSON-файл и возвращает список словарей
    с данными о финансовых транзакциях"""
    try:
        # Проверка на пустой файл не обязательна, т.к. json.load() сам вызовет JSONDecodeError
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):  # Проверка типа данных
            utils_logger.warning("Данные не являются списком!")
            return []
        return data
    except FileNotFoundError:
        utils_logger.error(f"Файл '{file_path}' не найден!")
        return []
    except json.JSONDecodeError:  # Ошибка формата JSON
        utils_logger.error("Invalid JSON data")
        return []


# if __name__ == "__main__":
#     data = load_json_data(file_path)
#     if data:
#         print("Данные загружены успешно!")
#     else:
#         print("Не удалось загрузить данные.")
