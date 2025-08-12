import re
from typing import List, Dict

from utils import load_json_data, json_file_path


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Функция принимает список словарей с данными о банковских операциями
    и список категорий операций, а возвращает словарь,
    в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории (description)"""
    if not data or not categories:
        return {}
    category_counts = {}

    for category in categories:
        try:
            pattern = re.compile(re.escape(category), flags=re.IGNORECASE)
            count = 0
            for transaction in data:
                if "description" in transaction and pattern.search(transaction["description"]):
                    count += 1
            category_counts[category] = count  # Всегда добавляем категорию, даже если count=0
        except re.error:
            # Для некорректных regex добавляем 0, чтобы сохранить согласованность
            category_counts[category] = 0

    return category_counts


def main():
    """Основная функция для выполнения при запуске скрипта"""
    transactions = load_json_data(json_file_path)

    if not transactions:
        print("Нет данных для обработки!")
    else:
        categories = ["Перевод", "Покупка", "Оплата"]
        counts = process_bank_operations(transactions, categories)
        print(counts)


if __name__ == "__main__":
    main()