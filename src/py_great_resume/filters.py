"""Custom filters for jinja2 templates."""
import datetime
import re

from markupsafe import Markup

RE_MD_INLINE_CODE = re.compile(r"(\W|^)(?:`)([\w-]+)(?:`)(\W|$)", flags=re.IGNORECASE)


def format_datetime(value: str, format_: str = "%Y-%m-%d") -> str:
    """Format ISO-compliant datetime string ``value`` according to ``format_`` spec."""
    try:
        dttm = datetime.datetime.fromisoformat(value)
    except ValueError:
        dttm = datetime.datetime.strptime(value, "%Y-%m")
    return dttm.strftime(format_)


def handle_md_inline_code(value: str) -> str:
    """Handle inline code md markup by wrapping contents in ``<code>`` tags."""
    if "`" in value and value.count("`") % 2 == 0:
        value = RE_MD_INLINE_CODE.sub(r"\1<code>\2</code>\3", value)
    return Markup(value)
