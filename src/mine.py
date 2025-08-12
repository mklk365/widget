from datetime import datetime

from utils import load_json_data, load_csv_data, load_xlsx_data, json_file_path, csv_file_path, xlsx_file_path
from masks import get_mask_card_number, get_mask_account


def mine():
    """Функция отвечает за основную логику проекта и связывает функциональности между собой"""
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )
    input_type_file = input()
    if input_type_file == "1":
        print("Для обработки выбран JSON-файл\n")
    elif input_type_file == "2":
        print("Для обработки выбран CSV-файл\n")
    elif input_type_file == "3":
        print("Для обработки выбран XLSX-файл\n")
    else:
        print(f"Операции с {input_type_file} недоступны")
        return None
    # Запрос статуса (в цикле, если введен неверный)
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        input_status = input().upper()
        if input_status in ("EXECUTED", "CANCELED", "PENDING"):
            print(f"Операции отфильтрованы по статусу '{input_status}'")
            break  # Выход из цикла, если статус верный
        else:
            print(f"Статус операции '{input_status}' недоступен.\n")  # Цикл продолжится
    # Запрос сортировки по дате
    print("\nОтсортировать операции по дате? Да/Нет")
    input_sort_by_date = False  # По умолчанию сортировка Не нужна
    input_sort_by_date_up = False  # По умолчанию сортировка по убыванию
    if input().lower() == "да":
        input_sort_by_date = True
        # Запрос сортировки по убыванию
        print("Отсортировать по возрастанию или по убыванию?")
        if input().lower() == "по возрастанию":
            input_sort_by_date_up = True
    # Запрос фильтрации по валюте
    print("\nВыводить только рублевые транзакции? Да/Нет")
    input_rub_only = input().lower() == "да"  # True, если "да", иначе False
    # Запрос фильтрации по слову в описании
    print("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет")
    input_filter_by_word = False
    input_filter_word = ""
    if input().lower() == "да":
        input_filter_by_word = True
        print("\nВведите слово для фильтрации")
        input_filter_word = input().lower()

    # Возвращаем полученные значения
    result = {
        "file_type": input_type_file,
        "status": input_status,
        "sort_by_date": input_sort_by_date,
        "rub_only": input_rub_only,
        "filter_by_word": input_filter_by_word,
    }
    # Возвращаем полученные значения, если есть фильтрация по слову в описании
    if input_sort_by_date:
        result["sort_by_date_up"] = input_sort_by_date_up
    if input_filter_by_word:
        result["filter_word"] = input_filter_word

    return result


def process_transactions(params, file_path=None):
    """Функция для обработки транзакций согласно параметрам"""
    # Загружаем данные в зависимости от типа файла
    if params["file_type"] == "1":
        transactions = load_json_data(file_path or json_file_path)
    elif params["file_type"] == "2":
        transactions = load_csv_data(file_path or csv_file_path)
    elif params["file_type"] == "3":
        transactions = load_xlsx_data(file_path or xlsx_file_path)
    else:
        return []

    if not transactions:
        print("Не удалось загрузить транзакции")
        return []

    # Фильтрация по статусу
    filtered_transactions = [t for t in transactions if t.get("state") == params["status"]]

    # Фильтрация по рублевым транзакциям
    if params["rub_only"]:
        filtered_transactions = [
            t for t in filtered_transactions if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]
    # Фильтрация по слову в описании
    if params["filter_by_word"]:
        filtered_transactions = [t for t in filtered_transactions if params["filter_word"] in t.get("description", "").lower()]
    # Сортировка по дате
    if params["sort_by_date"]:
        reverse_sort = not params["sort_by_date_up"]
        filtered_transactions.sort(key=lambda x: x.get("date", ""), reverse=reverse_sort)

    return filtered_transactions


def format_transaction(transaction):
    """Форматирует транзакцию для красивого вывода с использованием масок"""
    # Форматируем дату
    date_str = "Дата неизвестна"
    if "date" in transaction:
        try:
            # Пробуем разные форматы даты
            try:
                date_obj = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                date_obj = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S")
            date_str = date_obj.strftime("%d.%m.%Y")
        except (ValueError, TypeError):
            pass  # Оставляем "Дата неизвестна"

    description = transaction.get("description", "Без описания")

    # Форматируем отправителя (from)
    from_masked = ""
    if "from" in transaction:
        parts = transaction["from"].split()
        if len(parts) > 1:
            try:
                if parts[0] == "Счет":  # Это Счет
                    from_masked = f"Счет {get_mask_account(parts[-1])}"
                else:  # Это карта (Visa, MasterCard, Maestro и т.д.)
                    card_name = " ".join(parts[:-1])
                    from_masked = f"{card_name} {get_mask_card_number(parts[-1])}"
            except ValueError:  # Если маскировка не удалась (неправильный формат номера)
                from_masked = transaction["from"]  # Выводим исходные данные без маски

    # Форматируем получателя (to)
    to_masked = ""
    if "to" in transaction:
        parts = transaction["to"].split()
        if len(parts) > 1:
            try:
                if parts[0] == "Счет":  # Это Счет
                    to_masked = f"Счет {get_mask_account(parts[-1])}"
                else:  # Карта
                    card_name = " ".join(parts[:-1])
                    to_masked = f"{card_name} {get_mask_card_number(parts[-1])}"
            except ValueError:
                to_masked = transaction["to"]

    # Форматируем сумму и валюту
    amount_str = ""
    if "operationAmount" in transaction:
        amount = transaction["operationAmount"].get("amount", "0")
        currency = transaction["operationAmount"].get("currency", {}).get("name", "").replace("руб.", "руб.")
        amount_str = f"{float(amount):g} {currency}"  # :g убирает лишние нули

    # Собираем результат
    result = [f"{date_str} {description}"]

    if from_masked and to_masked:
        result.append(f"{from_masked} -> {to_masked}")
    elif to_masked:
        result.append(to_masked)

    result.append(f"Сумма: {amount_str}\n")

    return "\n".join(result)


def print_transactions(transactions):
    """Выводит список транзакций в консоль"""
    print("\nРаспечатываю итоговый список транзакций...\n")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}\n")
        for transaction in transactions:
            print(format_transaction(transaction))


def main():
    """Основная функция, обрабатывающая весь поток работы"""
    params = mine()
    if params is not None:
        result_transactions = process_transactions(params)
        print_transactions(result_transactions)

if __name__ == "__main__":
    main()

