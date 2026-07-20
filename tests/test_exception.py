import sys

import pytest

from safelink.exception.exception import SafeLinkException


def test_safelink_exception_captures_message_and_location():
    try:
        raise ValueError("boom")
    except Exception as e:
        exc = SafeLinkException(e, sys)

    text = str(exc)
    assert "boom" in text
    assert "line number" in text
    assert "python script name" in text
    # lineno should be a valid line number
    assert isinstance(exc.lineno, int)
    assert exc.lineno > 0


def test_safelink_exception_is_raisable():
    with pytest.raises(SafeLinkException):
        try:
            _ = 1 / 0
        except Exception as e:
            raise SafeLinkException(e, sys)