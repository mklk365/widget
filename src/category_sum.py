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
    # Создаем словарь для подсчета с нулевыми значениями для всех категорий
    category_counts = {category: 0 for category in categories}

    for transaction in data:
        if "description" not in transaction:
            continue

        description = transaction["description"]

        # Проверяем, соответствует ли описание какой-либо из категорий
        for category in categories:
            try:
                # Используем регулярное выражение для регистронезависимого поиска
                pattern = re.compile(re.escape(category), flags=re.IGNORECASE)
                if pattern.search(description):
                    category_counts[category] += 1
            except re.error:
                # В случае ошибки в регулярном выражении пропускаем эту категорию
                continue

    return category_counts


if __name__ == "__main__":
    # Загрузка данных
    transactions = load_json_data(json_file_path)

    if not transactions:
        print("Нет данных для обработки!")
    else:
        # Пример использования
        categories = ["Перевод", "Покупка", "Оплата"]
        counts = process_bank_operations(transactions, categories)
        print(counts)  # Выводит словарь с количеством операций по каждой категории