import pytest
from processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "value, state, expected",
    [
        # Фильтрация по EXECUTED
        (
            [
                {"id": 41428829, "state": "EXECUTED"},
                {"id": 594226727, "state": "CANCELED"},
                {"id": 41428821, "state": ""},
            ],
            "EXECUTED",
            [{"id": 41428829, "state": "EXECUTED"}],
        ),
        # Фильтрация по CANCELED
        (
            [
                {"id": 41428829, "state": "EXECUTED"},
                {"id": 594226727, "state": "CANCELED"},
                {"id": 41428821, "state": ""},
            ],
            "CANCELED",
            [{"id": 594226727, "state": "CANCELED"}],
        ),
        # Фильтрация если нет совпадений по CANCELED
        ([{"id": 41428829, "state": "EXECUTED"}, {"id": 41428821, "state": ""}], "CANCELED", []),
        # Фильтрация если пустой список
        ([], "CANCELED", []),
    ],
)
def test_filter_by_state(value, state, expected):
    assert filter_by_state(value, state) == expected


@pytest.mark.parametrize(
    "input_list, reverse_date, expected_output",
    [
        # Сортировка по убыванию даты
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        # Сортировка по возрастанию даты
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
        # Пустой список
        ([], True, []),
        # Одинаковые даты
        (
            [{"id": 1, "date": "2019-07-03T18:35:29.512364"}, {"id": 2, "date": "2019-07-03T18:35:29.512364"}],
            True,
            [{"id": 1, "date": "2019-07-03T18:35:29.512364"}, {"id": 2, "date": "2019-07-03T18:35:29.512364"}],
        ),
    ],
)
def test_sort_by_date(input_list, reverse_date, expected_output):
    """Тестирование основной функциональности сортировки по дате"""
    assert sort_by_date(input_list, reverse_date) == expected_output


@pytest.mark.parametrize(
    "input_list, error_message",
    [
        # Отсутствует ключ date
        ([{"id": 1}, {"id": 2, "date": "2019-07-03T18:35:29.512364"}], "Некорректная дата"),
        # Пустое значение даты
        ([{"id": 1, "date": ""}, {"id": 2, "date": "2019-07-03T18:35:29.512364"}], "Некорректная дата"),
        # None вместо даты
        ([{"id": 1, "date": None}, {"id": 2, "date": "2019-07-03T18:35:29.512364"}], "Некорректная дата"),
    ],
)
def test_sort_by_date_errors(input_list, error_message):
    """Тестирование обработки некорректных входных данных.
    Проверяет, что функция корректно выбрасывает ValueError при:
    - Отсутствии ключа 'date' в словаре
    - Пустом значении даты
    - Значении None в поле даты
    """
    with pytest.raises(ValueError, match=error_message):
        sort_by_date(input_list)


def test_sort_by_date_single_element():
    """Тестирование обработки списка с одним элементом.
    Проверяет, что:
    - Функция корректно обрабатывает список из одного элемента
    - Возвращается тот же список без изменений
    """
    input_list = [{"id": 1, "date": "2019-07-03T18:35:29.512364"}]
    assert sort_by_date(input_list) == input_list


def test_sort_by_date_does_not_modify_input():
    """Тестирование неизменяемости входного списка.
    Проверяет, что функция не изменяет переданный ей список,
    а возвращает новый отсортированный список.
    """
    input_list = [{"id": 2, "date": "2018-06-30T02:08:58.425572"}, {"id": 1, "date": "2019-07-03T18:35:29.512364"}]
    input_list_copy = input_list.copy()
    sort_by_date(input_list)
    assert input_list == input_list_copy
