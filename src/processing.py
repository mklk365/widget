from typing import List, Dict, Any


def filter_by_state(list_dict: List[Dict[str, int]], state: str = "EXECUTED") -> List[Dict[str, int]]:
    """Функция принимает список словарей и опционально значение для ключа"""
    select_dict = []
    for i in list_dict:
        if i["state"] == state:
            select_dict.append(i)
    return select_dict


def sort_by_date(list_dict: List[Dict[str, int]], reverse_date: bool = True) -> List[Dict[str, int]]:
    """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки"""
    for item in list_dict:
        if not item.get("date"):
            raise ValueError("Некорректная дата")
    sorted_list = sorted(list_dict, key=lambda rec: rec["date"], reverse=reverse_date)
    return sorted_list
