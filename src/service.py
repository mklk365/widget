from typing import Dict, Any


def dict_is_none(data: Dict[str, Any]):
    """Проверка на пустой словарь"""
    if data:
        return data
    raise ValueError("Словарь пустой")
