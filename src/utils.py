import json
import os

file_path = os.path.join("..", "data", "operations.json")  # путь к JSON


def load_json_data(file_path):
    try:
        if os.path.getsize(file_path) == 0:  # Проверка пустой ли файл
            print("Файл пуст!")
            return []
        with open(file_path, "r", encoding="utf-8") as f:  # Открытие файла и загрузка JSON
            data = json.load(f)
            if type(data) != list:  # Проверка типа данных
                print("Данные не являются списком!")
                return []
            return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден!")
        return []
    except json.JSONDecodeError:  # Когда строка имеет неправильный формат, некорректные символы или другие ошибки
        print("Invalid JSON data")
        return []


if __name__ == "__main__":
    data = load_json_data(file_path)
    if data:  # Проверка что список не пустой
        print("Данные загружены успешно!")
    else:
        print("Не удалось загрузить данные.")
