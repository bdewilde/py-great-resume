import pytest

from py_great_resume import filters


@pytest.mark.parametrize(
    "value, format_, exp",
    [
        ("2021-01-01T00:00:00", "%Y-%m-%d", "2021-01-01"),
        ("2021-01-01", "%Y-%m-%d", "2021-01-01"),
        ("2021-01", "%Y-%m-%d", "2021-01-01"),
        ("2021-01-01T00:00:00", "%b %Y", "Jan 2021"),
        ("2021-01-01", "%b %Y", "Jan 2021"),
        ("2021-01", "%b %Y", "Jan 2021"),
    ]
)
def test_format_datetime(value, format_, exp):
    obs = filters.format_datetime(value, format_)
    assert exp == obs


@pytest.mark.parametrize(
    "value, exp",
    [
        ("foo `bar` bat", "foo <code>bar</code> bat"),
        ("foo`bar`bat", "foo`bar`bat"),
        ("foo `bar bat", "foo `bar bat"),
    ]
)
def test_handle_md_inline_code(value, exp):
    obs = filters.handle_md_inline_code(value)
    assert exp == obs
