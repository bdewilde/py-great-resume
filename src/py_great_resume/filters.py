"""Custom filters for jinja2 templates."""
import datetime
import re

import jinja2


RE_MD_INLINE_CODE = re.compile(r"(`)([\w-]+)(`)", flags=re.IGNORECASE)


def format_datetime(value: str, format_: str = "%Y-%m-%d") -> str:
    """Format ISO-compliant datetime string ``value`` according to ``format_`` spec."""
    try:
        value = datetime.datetime.fromisoformat(value)
    except ValueError:
        value = datetime.datetime.strptime(value, "%Y-%m")
    return value.strftime(format_)


def handle_md_inline_code(value: str) -> str:
    """Handle inline code md markup by wrapping contents in ``<code>`` tags."""
    if "`" not in value or value.count("`") % 2 != 0:
        return value
    else:
        return jinja2.Markup(RE_MD_INLINE_CODE.sub(r"<code>\2</code>", value))
