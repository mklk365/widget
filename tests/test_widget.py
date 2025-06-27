import pytest
from src.widget import mask_account_card, get_date

@pytest.mark.parametrize("value, answer", [("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"), ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"), ("Счет 73654108430135874305", "Счет **4305")])
def test_mask_account_card(value, answer):
    assert mask_account_card(value) == answer
    with pytest.raises(ValueError, match="Некорректный номер"):
        mask_account_card("Visa Platinum 7")
    with pytest.raises(ValueError, match="Некорректный номер"):
        mask_account_card("")

def test_get_date_fixture(list_date_test):
    assert get_date(list_date_test) == '11.03.2024'
    with pytest.raises(ValueError, match="Некорректная дата"):
        get_date("2024-03-1")
    with pytest.raises(ValueError, match="Некорректная дата"):
        get_date("")
