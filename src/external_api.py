import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

from service import dict_is_none


def convert_apilayer_data(amount: str, code_from: str, code_to: str) -> float:
    """Функция обращения к внешнему API для получения
    текущего курса валют и конвертации суммы операции в рубли"""
    load_dotenv()  # Загрузка переменных из .env-файла
    apikey = os.getenv("API_KEY")  # Получение значения переменной API_KEY из .env-файла
    if not apikey:
        raise ValueError("API_KEY не найден в .env файле")
    headers = {"apikey": apikey}
    payload = {}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={code_to}&from={code_from}&amount={amount}"
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        result = response.text
        if status_code != 200:
            raise Exception(f"Ошибка api: {status_code} - {result}")
        output_data = response.json()  # Преобразование ответа сервера в объект Python
        output_data_result = round(output_data["result"], 2)  # Округление результата
        return float(output_data_result)
    except Exception as e:
        raise Exception(f"Что-то пошло не так: {str(e)}")


def get_transaction_amount(transaction: Dict[str, Any]) -> float:
    """Функция принимает на вход транзакцию
    и возвращает сумму транзакции (amount) в рублях(float)"""
    dict_is_none(transaction)  # Проверка на пустой словарь
    try:
        operation_amount = transaction.get("operationAmount", {})  # Получаем вложенный словарь operationAmount
        currency = operation_amount.get("currency", {})
        currency_code = currency.get("code")
        amount_data = operation_amount.get("amount", 0)
        if currency_code == "RUB":
            return float(amount_data)
        else:
            return convert_apilayer_data(amount=amount_data, code_from=currency_code, code_to="RUB")
    except Exception as e:
        raise Exception(f"Что-то пошло не так: {str(e)}")


# if __name__ == "__main__":
#     #   """ Проверки """
#     print(get_transaction_amount({}))
#
#     # """Проверка ответа сервиса при передаче явных данных"""
#     # print(convert_apilayer_data(amount="1200", code_to="USD", code_from="RUB"))
#
#     # """Проверка конвертации при передаче данных из файла.json"""
#     # from src.utils import load_json_data
#     # file_path = os.path.join('..', 'data', 'operations.json')  # путь к JSON
#     # transactions = load_json_data(file_path)
#     # print(get_transaction_amount(transactions[0]))
