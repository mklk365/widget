import json
import os

file_path = os.path.join("..", "data", "operations.json")  # путь к JSON


def load_json_data(file_path):
    try:
        # Проверка на пустой файл не обязательна, т.к. json.load() сам вызовет JSONDecodeError
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):  # Проверка типа данных
            print("Данные не являются списком!")
            return []

        return data

    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден!")
        return []
    except json.JSONDecodeError:  # Ошибка формата JSON
        print("Invalid JSON data")
        return []


# if __name__ == "__main__":
#     data = load_json_data(file_path)
#     if data:  # Проверка что список не пустой
#         print("Данные загружены успешно!")
#     else:
#         print("Не удалось загрузить данные.")
