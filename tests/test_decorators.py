import pytest
from datetime import datetime

from decorators import log


@log()
def successful_func():
    return "Success!"

@log()
def failing_func():
    raise ValueError("Test error")

def test_start_message_is_printed(capsys):
    """Проверяем, что в stdout выводится 'Start:'"""
    successful_func()
    captured = capsys.readouterr()
    assert "Start:" in captured.out

def test_error_message_is_printed_on_exception(capsys):
    """Проверяем, что при ошибке выводится сообщение с её текстом"""
    with pytest.raises(ValueError):
        failing_func()
    captured = capsys.readouterr()
    assert "Error:" in captured.out
    assert "Test error" in captured.out
