import pytest

@pytest.fixture
def list_date_test():
    return '2024-03-11T02:26:18.671407'

@pytest.fixture
def list_tranzact_test():
    return [{
        "id": 939719570,
        "operationAmount": {
            "currency": {
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "to": "Счет 11776614605963066702"
    }]