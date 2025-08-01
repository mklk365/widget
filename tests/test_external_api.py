import pytest
from unittest.mock import patch, Mock
from external_api import convert_apilayer_data, get_transaction_amount


def test_convert_apilayer_data_success():
    """Тест успешного ответа от API: Мокаем requests.request, чтобы он возвращал успешный JSON-ответ"""
    mock_response = Mock()  # Подготовка мок-ответа
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 75.50}

    with patch("requests.request", return_value=mock_response) as mock_request:
        result = convert_apilayer_data("1", "USD", "RUB")
        assert result == 75.50
        mock_request.assert_called_once()  # Проверяет, была ли функция вызвана только один раз


def test_convert_apilayer_data_api_error():
    """Тест обработки ошибки API"""
    mock_response = Mock()  # Подготовка мок-ответа
    mock_response.status_code = 400
    mock_response.text = "Ошибка api"

    with patch("requests.request", return_value=mock_response):
        with pytest.raises(Exception, match="Ошибка api: 400 - Ошибка api"):
            convert_apilayer_data("1", "USD", "RUB")


def test_same_currency():
    """Тест одинаковых валют"""
    mock_response = Mock()  # Подготовка мок-ответа
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 1.0}

    with patch("requests.request", return_value=mock_response):
        result = convert_apilayer_data("1", "USD", "USD")
        assert result == 1.0


def test_missing_api_key():
    """Тест отсутствия API-ключа в .env"""
    with patch("os.getenv", return_value=None):
        with pytest.raises(ValueError, match="API_KEY не найден в .env файле"):
            convert_apilayer_data("1", "USD", "RUB")


def test_get_transaction_amount_rub():
    """Тест на корректное извлечение суммы в RUB"""
    transaction = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}
    assert get_transaction_amount(transaction) == 100.50


def test_get_transaction_empty_transaction():
    """Тест на пустую транзакцию"""
    with pytest.raises(Exception):
        get_transaction_amount({})


def test_get_transaction_invalid_amount():
    """Тест на неверный формат суммы"""
    transaction = {"operationAmount": {"amount": "сто", "currency": {"code": "RUB"}}}
    with pytest.raises(Exception):
        get_transaction_amount(transaction)


@pytest.mark.parametrize("amount,expected", [("0", 0.0), ("1000000", 1000000.0)])
def test_get_transaction_amount_boundary_values(amount, expected):
    """Тест граничных значений суммы"""
    transaction = {"operationAmount": {"amount": amount, "currency": {"code": "RUB"}}}
    assert get_transaction_amount(transaction) == expected


def test_get_transaction_amount_missing_operation_amount():
    """Тест отсутствия operationAmount в транзакции"""
    with pytest.raises(Exception):
        get_transaction_amount({"some_other_field": "value"})


def test_get_transaction_amount_missing_currency():
    """Тест отсутствия currency в operationAmount"""
    with pytest.raises(Exception):
        get_transaction_amount({"operationAmount": {"amount": "100"}})


def test_get_transaction_amount_foreign_currency():
    """Тест конвертации иностранной валюты"""
    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    with patch("external_api.convert_apilayer_data", return_value=75.0) as mock_convert:
        result = get_transaction_amount(transaction)
        assert result == 75.0
        mock_convert.assert_called_once_with(amount="10", code_from="USD", code_to="RUB")


def test_get_transaction_amount_api_error_propagation():
    """Тест пробрасывания ошибки от convert_apilayer_data"""
    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    with patch("external_api.convert_apilayer_data", side_effect=Exception("API error")):
        with pytest.raises(Exception, match="Что-то пошло не так: API error"):
            get_transaction_amount(transaction)
