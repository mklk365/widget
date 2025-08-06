import logging
import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Путь к папке logs
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")  # Путь к корневой папке logs
LOG_FILE = os.path.join(LOG_DIR, "masks_logger.log")  # Полный путь к файлу лога
os.makedirs(LOG_DIR, exist_ok=True)  # Создаем папку logs, если её нет

# Настройка логгера (перед использованием в функциях)
masks_logger = logging.getLogger(__name__)  # Создание и получение именованного логера
masks_logger.setLevel(logging.DEBUG)  # Настройка уровня логгирования
masks_logger.handlers = []  # Очистка старых обработчиков
# Создаем хендлер для вывода в файл
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")  # Новый лог при каждом запуске
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
masks_logger.addHandler(file_handler)


# Принудительно пишем тестовое сообщение
masks_logger.info("Логгер инициализирован!")


def get_mask_card_number(card_number: str | int) -> str:
    """Функция принимает номер карты и возвращает ее маску"""
    masks_logger.info(f"Вызов get_mask_card_number с аргументом: {card_number}")
    str_number = str(card_number)
    if len(str_number) != 16 or not str_number.isdigit():
        error_msg = "Некорректный номер карты"
        masks_logger.error(f"Ошибка в get_mask_card_number: {error_msg} (входные данные: {card_number})")
        raise ValueError(error_msg)
    masked_number = f"{str_number[0:4]} {str_number[4:6]}** **** {str_number[12:16]}"
    masks_logger.info(f"Успешная маскировка карты: {masked_number}")
    return masked_number


def get_mask_account(schet_number: str | int) -> str:
    """Функция принимает номер счета и возвращает его маску"""
    masks_logger.info(f"Вызов get_mask_account с аргументом: {schet_number}")
    str_number = str(schet_number)

    if len(str_number) != 20 or not str_number.isdigit():
        error_msg = "Некорректный номер счета"
        masks_logger.error(f"Ошибка в get_mask_account: {error_msg} (входные данные: {schet_number})")
        raise ValueError(error_msg)

    masked_account = f"**{str_number[-4:]}"
    masks_logger.info(f"Успешная маскировка счета: {masked_account}")
    return masked_account
