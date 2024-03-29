from __future__ import annotations

import io
import json
import logging
import os
import urllib.request
from typing import Any, Dict, Optional, Union

import jinja2
import jsonschema
import weasyprint

from . import filters

LOGGER = logging.getLogger(__name__)


class Resume:
    """
    Class for loading a resume from JSON, validating it against a schema, and
    exporting it to HTML or PDF.

    .. code-block:: pycon

        >>> resume = py_great_resume.Resume("/path/to/resume.json", template="long")
        >>> resume.validate()
        >>> resume.to_pdf("/path/to/resume.pdf")
        >>> resume.to_html("/path/to/resume.html")

    Source resume data is expected to follow the `JSON Resume <https://jsonresume.org>`_
    schema. According to `JSON Schema <http://json-schema.org/>`_, it's best practice
    to embed a link to the schema specification within the source data itself using
    a top-level ``"$schema"`` field. This field is used by :meth:`Resume.validate()`.
    """

    def __init__(self, data_fpath: str | os.PathLike, *, template: str = "long"):
        self.env = self._init_environment()
        self.template = self.env.get_template(f"{template}.html")
        self.data = self._load_json_data(data_fpath)

    def _init_environment(self) -> jinja2.Environment:
        env = jinja2.Environment(
            loader=jinja2.PackageLoader("py_great_resume", "templates"),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters["format_datetime"] = filters.format_datetime
        env.filters["handle_md_inline_code"] = filters.handle_md_inline_code
        return env

    def validate(self, schema: Optional[Union[str, Dict[str, Any]]] = None):
        if schema is None:
            try:
                schema = self.data["$schema"]
            except KeyError:
                LOGGER.error(
                    "a schema must be specified for validation, either as method arg "
                    "or '$schema' key in json resume data"
                )
                raise
        if isinstance(schema, str):
            schema = self._request_json_data(url=schema)
        try:
            jsonschema.validate(self.data, schema)
            LOGGER.info("resume JSON data is valid!")
        except (jsonschema.ValidationError, jsonschema.SchemaError):
            LOGGER.exception("unable to validate JSON data")
            raise

    def to_html(self, fpath: str | os.PathLike):
        html_str = self.template.render(self.data)
        with io.open(fpath, mode="wt") as f:
            f.write(html_str)
        LOGGER.info("resume saved as HTML to %s", fpath)

    def to_pdf(self, fpath: str | os.PathLike):
        html_str = self.template.render(self.data)
        html = weasyprint.HTML(string=html_str)
        html.write_pdf(fpath)
        LOGGER.info("resume saved as PDF to %s", fpath)

    def _load_json_data(self, fpath: str | os.PathLike) -> Dict[str, Any]:
        with io.open(fpath, mode="rt") as f:
            data = json.load(f)
        return data

    def _request_json_data(self, url: str):
        with urllib.request.urlopen(url) as resp:
            html = resp.read().decode(resp.headers.get_param("charset") or "utf-8")
        return json.loads(html)
