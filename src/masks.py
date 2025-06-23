from typing import Any


def get_mask_card_number(card_number: Any) -> str:
    """Функция принимает номер карты и возвращает ее маску"""
    str_number = str(card_number)
    if len(str_number) != 16 or not str_number.isdigit():
        raise ValueError("Некорректный номер карты")
    return f"{str_number[0:4]} {str_number[4:6]}** **** {str_number[12:16]}"


def get_mask_account(schet_number: Any) -> str:
    """Функция принимает номер счета и возвращает его маску"""
    str_number = str(schet_number)
    if len(str_number) != 20 or not str_number.isdigit():
        raise ValueError("Некорректный номер счета")
    return f"**{str_number[-4:]}"
