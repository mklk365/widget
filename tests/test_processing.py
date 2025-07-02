import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.mark.parametrize("value, state, expected", [
    # Фильтрация по EXECUTED
    ([{'id': 41428829, "state": "EXECUTED"},
    {'id': 594226727, "state": "CANCELED"},
    {'id': 41428821, "state": ""}],
    "EXECUTED",
    [{'id': 41428829, "state": "EXECUTED"}]),
    # Фильтрация по CANCELED
    ([{'id': 41428829, "state": "EXECUTED"},
      {'id': 594226727, "state": "CANCELED"},
      {'id': 41428821, "state": ""}],
     "CANCELED",
     [{'id': 594226727, "state": "CANCELED"}]),
    # Фильтрация если нет совпадений по CANCELED
    ([{'id': 41428829, "state": "EXECUTED"},
    {'id': 41428821, "state": ""}],
     "CANCELED",
     []),
    # Фильтрация если пустой список
    ([],
     "CANCELED",
     [])
    ])
def test_filter_by_state(value, state, expected):
    assert filter_by_state(value, state) == expected


@pytest.mark.parametrize("input_list, reverse_date, expected_output", [
    # Сортировка по убыванию даты
    ([
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ],
    True,
    [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]),
    # Сортировка по возрастанию даты
    ([
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ],
    False,
    [
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    ]),
    # Пустой список
    ([],
        True,
    []),
    # Одинаковые даты
    ([
    {'id': 1, 'date': '2019-07-03T18:35:29.512364'},
    {'id': 2, 'date': '2019-07-03T18:35:29.512364'}
    ],
    True,
    [
    {'id': 1, 'date': '2019-07-03T18:35:29.512364'},
    {'id': 2, 'date': '2019-07-03T18:35:29.512364'}
    ])
    ])
def test_sort_by_date(input_list, reverse_date, expected_output):
    assert sort_by_date(input_list, reverse_date) == expected_output
