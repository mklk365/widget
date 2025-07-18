import os
import pytest

from decorators import log


def test_log_to_file():
    """Тест записи логов в файл"""
    test_filename = "test_log.txt"

    @log(filename=test_filename)
    def successful_func():  # Объявление успешной функции
        return "Success!"

    result = successful_func()  # Вызов успешной функции

    assert os.path.exists(test_filename)  # Проверка создания файла

    with open(test_filename, "r") as f:
        content = f.read()
    assert "Start:" in content  # Проверки наличия записей
    assert "Result: Success!" in content
    assert "End:" in content

    os.remove(test_filename)  # Удаление файла


def test_log_err_to_file():
    """Тест записи ошибки в файл"""
    test_filename = "test_log.txt"

    @log(filename=test_filename)
    def failing_func():  # Объявление ошибочной функции
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        failing_func()  # Вызов ошибочной функции

    assert os.path.exists(test_filename)  # Проверка создания файла

    with open(test_filename, "r") as f:
        content = f.read()
    assert "Start:" in content  # Проверки наличия записей
    assert "Name: failing_func error" in content
    assert "Error: Test error" in content
    assert "End:" in content

    os.remove(test_filename)  # Удаление файла


def test_log_in_console(capsys):
    """Тест вывода логов в консоль"""

    @log()
    def successful_func():
        return "Success!"

    successful_func()  # Вызов успешной функции
    captured = capsys.readouterr()
    output = captured.out

    assert "Start:" in output
    assert "Name: successful_func ok" in output
    assert "Result: Success!" in output
    assert "End:" in output


def test_log_err_in_console(capsys):
    """Тест вывода ошибки в консоль"""

    @log()
    def failing_func():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        failing_func()  # Вызов ошибочной функции
    captured = capsys.readouterr()
    output = captured.out

    assert "Start:" in output
    assert "Name: failing_func error" in output
    assert "Error: Test error" in output
    assert "End:" in output


