import re
from typing import List, Dict

from utils import load_json_data, json_file_path


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Функция принимает список словарей с данными о банковских операциях (JSON-файл)
    и строку поиска и возвращает список словарей,
    у которых в описании есть данная строка"""
    if not data:
        return []
    try:
        pattern = re.compile(search, flags=re.IGNORECASE)
    except re.error as e:
        print(f"Ошибка в регулярном выражении: {e}")
        return []
    return [transaction for transaction in data if "description" in transaction and pattern.search(transaction["description"])]


# if __name__ == "__main__":
#     # Загрузка данных
#     transactions = load_json_data(json_file_path)
#
#     if not transactions:
#         print("Нет данных для обработки!")
#     else:
#         # Примеры поиска (регистронезависимо):
#         coffee_transactions = process_bank_search(transactions, r"Перевод")
#         print(coffee_transactions)  # Для проверки выводим результат
