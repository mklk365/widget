def get_mask_card_number(card_number: Any) -> str:
    """Функция принимает номер карты и возвращает ее маску"""
    str_number = str(card_number)
    return f"{str_number[0:4]} {str_number[4:6]} **** {str_number[12:16]}"


def get_mask_account(schet_number: Any) -> str:
    """Функция принимает номер счета и возвращает его маску"""
    str_number = str(schet_number)
    return f"*{str_number[-4:]}"
