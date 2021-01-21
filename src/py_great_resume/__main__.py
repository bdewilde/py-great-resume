import argparse
import pathlib

import py_jsonresume


def add_and_parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="command line interface for py_jsonresume",
    )
    parser.add_argument(
        "--src_fpath", type=pathlib.Path, required=True,
        help="path to file on disk where source json resume data is saved",
    )
    parser.add_argument(
        "--tgt_fpath", type=pathlib.Path, required=True,
        help="path to file on disk where target html/pdf resume data is to be saved",
    )
    parser.add_argument(
        "--template", type=str, default="long", choices=("long",),
        help="name of template into which resume data will be inserted, as found in "
        "the `/templates` directory"
    )
    parser.add_argument(
        "--validate", action="store_true", default=False,
        help="flag that specifies whether source json resume data is to be validated "
        "against a schema, specified internally or via `--schema_url` arg"
    )
    parser.add_argument(
        "--schema_url", type=str, default=None,
        help="url of schema against which source json resume data is to be validated; "
        "NOTE: only used if `--validate` is specified"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = add_and_parse_args()
    jr = py_jsonresume.JsonResume(str(args.src_fpath), template=args.template)
    if args.validate is True:
        jr.validate(schema=args.schema_url)
    if args.tgt_fpath.suffix == ".html":
        jr.to_html(args.tgt_fpath)
    if args.tgt_fpath.suffix == ".pdf":
        jr.to_pdf(args.tgt_fpath)