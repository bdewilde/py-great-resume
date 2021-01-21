import argparse
import pathlib

import py_jsonresume


def add_and_parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="command line interface for py_jsonresume",
    )
    parser.add_argument("--src_fpath", type=pathlib.Path, required=True)
    parser.add_argument("--tgt_fpath", type=pathlib.Path, required=True)
    parser.add_argument("--template", type=str, default="long", choices=("long",))
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = add_and_parse_args()
    jr = py_jsonresume.JsonResume(str(args.src_fpath), template=args.template)
    if args.tgt_fpath.suffix == ".html":
        jr.to_html(args.tgt_fpath)
    if args.tgt_fpath.suffix == ".pdf":
        jr.to_pdf(args.tgt_fpath)
