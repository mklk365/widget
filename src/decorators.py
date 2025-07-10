from datetime import datetime
from functools import wraps
import os


def log(filename=None):
    """Декоратор логирует начало и конец выполнения функции,
    а также ее результаты или возникшие ошибки.
    Принимает необязательный аргумент filename, который определяет,
    куда будут записываться логи (в файл или в консоль)"""

    def log_decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time_start = datetime.now()
            start_msg = f"Name:  {func.__name__}\nStart: {time_start}"
            print(start_msg)
            if filename:
                with open(filename, 'a') as file:
                    file.write(start_msg + '\n')
            try:
                result = func(*args, **kwargs)  # Вызов исходной функции
                time_end = datetime.now()
                result_msg = f"End:   {time_end}\nResult: {result}"
                print(result_msg)
                if filename:
                    with open(filename, 'a') as file:
                        file.write(result_msg + '\n')
                return result
            except Exception as e:
                time_end = datetime.now()
                err_msg = f"End:   {time_end}\nError: {e}"
                print(err_msg)
                if filename:
                    with open(filename, 'a') as file:
                        file.write(err_msg + '\n')
                raise

        return wrapper

    return log_decor
