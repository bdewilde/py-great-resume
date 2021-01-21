import io
import json
from typing import Any, Dict

import jinja2
import weasyprint

from py_jsonresume import filters


class JsonResume:

    def __init__(self, data_fpath: str, *, template: str = "long"):
        self.env = self._init_environment()
        self.template = self.env.get_template(f"{template}.html")
        self.data = self._load_json_data(data_fpath)

    def _init_environment(self) -> jinja2.Environment:
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("py_jsonresume", "templates"),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters["format_datetime"] = filters.format_datetime
        env.filters["handle_md_inline_code"] = filters.handle_md_inline_code
        return env

    def _load_json_data(self, fpath: str) -> Dict[str, Any]:
        with io.open(fpath, mode="rt") as f:
            data = json.load(f)
        return data

    def to_html(self, fpath: str):
        html_str = self.template.render(data)
        with io.open(fpath, mode="wt") as f:
            f.write(html)

    def to_pdf(self, fpath: str):
        html_str = self.template.render(data)
        html = weasyprint.HTML(string=html_str)
        html.write_pdf(fpath)
