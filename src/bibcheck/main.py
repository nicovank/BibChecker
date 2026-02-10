import argparse
import sys

from .bibliography import Bibliography
from .utils import exclusions, load_source_patterns

def run(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Parse bibcheck options")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("-write_out", action="store_true", help="Save output to a .doc file")

    style_group = parser.add_mutually_exclusive_group()
    style_group.add_argument("-ieee", action="store_true", help="Parse IEEE style references")
    style_group.add_argument("-acm", action="store_true", help="Parse ACM style references")
    style_group.add_argument("-siam", action="store_true", help="Parse SIAM style references")
    style_group.add_argument("-springer", action="store_true", help="Parse Springer style references")


    parser.add_argument(
        "--exclude-file",
        action="append",
        default=[],
        metavar="PATH",
        help="JSON file with additional exclusions (can be passed multiple times).",
    )

    args = parser.parse_args(argv)

    exclusions = load_source_patterns(extra_files=args.exclude_file)


    bib = Bibliography()
    if bib.parse(args):
        bib.validate(args)

if __name__ == "__main__":
    run()

