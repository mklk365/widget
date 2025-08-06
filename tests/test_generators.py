import pytest
from generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.mark.parametrize(
    "value, code, expected",
    [
        # Фильтрация по USD
        (
            [
                {
                    "id": 939719570,
                    "operationAmount": {"currency": {"code": "USD"}},
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 873106923,
                    "operationAmount": {"currency": {"code": "RUB"}},
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
            ],
            "USD",
            [
                {
                    "id": 939719570,
                    "operationAmount": {"currency": {"code": "USD"}},
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                }
            ],
        ),
        # Фильтрация по RUB
        (
            [
                {
                    "id": 939719570,
                    "operationAmount": {"currency": {"code": "USD"}},
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 873106923,
                    "operationAmount": {"currency": {"code": "RUB"}},
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
            ],
            "RUB",
            [
                {
                    "id": 873106923,
                    "operationAmount": {"currency": {"code": "RUB"}},
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                }
            ],
        ),
        # Фильтрация если пустой список
        ([], "RUB", []),
    ],
)
def test_filter_by_currency(value, code, expected):
    assert list(filter_by_currency(value, code)) == expected


def test_transaction_descriptions(list_tranzact_test):
    gen = transaction_descriptions(list_tranzact_test)
    assert next(gen) == "Перевод организации"


@pytest.mark.parametrize(
    "start, end, expected_output",
    [
        # На вход подается корректный диапазон
        (5, 6, ["0000 0000 0000 0005", "0000 0000 0000 0006"]),
        (666, 667, ["0000 0000 0000 0666", "0000 0000 0000 0667"]),
        (100100500, 100100501, ["0000 0001 0010 0500", "0000 0001 0010 0501"]),
    ],
)
def test_card_number_generator(start, end, expected_output):
    assert card_number_generator(start, end) == expected_output


@pytest.mark.parametrize(
    "start, end, expected_exception",
    [
        # Некорректные данные
        (5, "q", ValueError),
        ("s", 20, ValueError),
        (0, 5, ValueError),
        (-1, 3, ValueError),
        (1, -3, ValueError),
        # Start больше End
        (10, 5, ValueError),
        # Слишком большие числа
        (1, 10000000000000000, ValueError),
    ],
)
def test_card_number_generator_errors(start, end, expected_exception):
    with pytest.raises(expected_exception):
        card_number_generator(start, end)
