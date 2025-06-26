from .masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_schet_number: str) -> str:
    """Функция обрабатывает информацию о картах и счетах"""
    digit_number = ""
    alpfa_number = ""
    digit_for_mask = ""
    for i in card_or_schet_number:
        if i.isdigit():
            digit_number += i
        elif not i.isdigit():
            alpfa_number += i
    if len(digit_number) == 16:
        digit_for_mask = get_mask_card_number(digit_number)
    elif len(digit_number) == 20:
        digit_for_mask = get_mask_account(digit_number)
    return f"{alpfa_number}{digit_for_mask}"


def get_date(date_original: str) -> str:
    """Функция обрабатывает строку с датой в новый формат"""
    if len(date_original) < 12:
        raise ValueError("Некорректная дата")
    date_ready = date_original[8:10] + "." + date_original[5:7] + "." + date_original[0:4]
    return date_ready
