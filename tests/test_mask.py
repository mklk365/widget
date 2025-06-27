import pytest
from src.masks import get_mask_card_number, get_mask_account

def test_mask_card_number():
    assert get_mask_card_number('7000792289606361') == '7000 79** **** 6361'
    with pytest.raises(ValueError, match="Некорректный номер"):
        get_mask_card_number('70007922896')
    with pytest.raises(ValueError, match="Некорректный номер"):
        get_mask_card_number("")

def test_get_mask_account():
    assert get_mask_account('73654108430135874305') == '**4305'
    with pytest.raises(ValueError, match="Некорректный номер"):
        get_mask_account('70007922896')
    with pytest.raises(ValueError, match="Некорректный номер"):
        get_mask_account("")
