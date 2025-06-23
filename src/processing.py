from typing import List, Dict, Any


def filter_by_state(list_dict, state="EXECUTED") -> List[Dict[str, Any]]:
    """Функция принимает список словарей и опционально значение для ключа"""
    select_dict = []
    for i in list_dict:
        if i["state"] == state:
            select_dict.append(i)
    return select_dict


def sort_by_date(list_dict, reverse_date=True) -> List[Dict[str, Any]]:
    """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки"""
    sorted_list = sorted(list_dict, key=lambda rec: rec["date"], reverse=reverse_date)
    return sorted_list
