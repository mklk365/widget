import pytest
from decorators import log


def test_log():
    @log
    def get_mask_account(num_acc):
        return num_acc

    result = get_mask_account('73654108430135874305')
    assert result == '**4305'