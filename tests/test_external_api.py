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
        with pytest.raises(Exception, match="Что-то пошло не так"):
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
