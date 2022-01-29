#!/usr/bin/env python3
"""Convert the wordle squares to something different"""

import argparse
import sys


def convert_text(in_text, miss_char, wrong_place_char, right_place_char):
    replacements = {
        "⬛": miss_char,
        "🟨": wrong_place_char,
        "🟩": right_place_char,
    }
    out_text = []
    for char in in_text:
        out_text.append(replacements.get(char, char))
    return "".join(out_text)


def parse_char(char):
    """Convert a replacement character into unicode"""
    if len(char) != 1:
        raise ValueError("Expecting string of length 1")
    return char


def parse_replace(replace):
    """Convert a replacement string into three parts"""
    if len(replace) != 3:
        raise ValueError("Expecting string of length 3")
    return replace


def main(inputfile=None, miss=None, wrong=None, right=None, replace=None):
    """
    Process the command line and run the conversion.

    Arguments:
    inputfile -- An input stream, defaults to sys.stdin
    miss -- The replacement character for ⬛, a missed letter
    wrong -- The replacement for 🟨, a matching letter in the wrong place
    right -- The replacement for 🟩, a matching letter in the right place
    replace -- A triple for miss, wrong, right

    Return is a tuple:
    output - The converted input, or None if errors
    errors - A list of errors encountered while processing the command
    """
    errors = []
    in_text = None
    inputfile = inputfile or sys.stdin
    if inputfile.isatty():
        errors.append("Must specify an inputfile or pipe the input")
    else:
        in_text = inputfile.read()

    # Determine the replacements
    miss_char, wrong_char, right_char = (None, None, None)
    if replace:
        if miss:
            errors.append("Can not use --miss and --replace")
        if wrong:
            errors.append("Can not use --wrong and --replace")
        if right:
            errors.append("Can not use --right and --replace")
        if not any((miss, wrong, right)):
            try:
                miss_char, wrong_char, right_char = parse_replace(replace)
            except ValueError as err:
                errors.append("Unable to parse --replace")
    elif all((miss, wrong, right)):
        try:
            miss_char = parse_char(miss)
        except ValueError:
            errors.append("Unable to parse -m/--miss")
        try:
            wrong_char = parse_char(wrong)
        except ValueError:
            errors.append("Unable to parse -w/--wrong")
        try:
            right_char = parse_char(right)
        except ValueError:
            errors.append("Unable to parse -r/--right")
    elif not any((miss, wrong, right)):
        errors.append(
            "Must specify replacements with --replace or --miss, --wrong, and --right"
        )
    else:
        if not miss:
            errors.append("Must specify -m/--miss")
        if not wrong:
            errors.append("Must specify -w/--wrong")
        if not right:
            errors.append("Must specify -r/--right")

    if errors:
        return None, errors
    else:
        out_text = convert_text(in_text, miss_char, wrong_char, right_char)
        return out_text, errors


def get_parser():
    """Get the command line parser"""
    parser = argparse.ArgumentParser(
        description="Convert a wordle result to something different"
    )
    parser.add_argument(
        "inputfile",
        nargs="?",
        help="An input file with a Wordle result. Alternatively, pipe the text to the program.",
        type=argparse.FileType("r"),
    )
    parser.add_argument("-m", "--miss", help="The replacement for ⬛, a missed letter")
    parser.add_argument(
        "-w",
        "--wrong",
        help="The replacement for 🟨, a matching letter in the wrong place",
    )
    parser.add_argument(
        "-r",
        "--right",
        help="The replacement for 🟩, a matching letter in the right place",
    )
    parser.add_argument("--replace", help="The three replacements, in ⬛🟨🟩 order")
    return parser


if __name__ == "__main__":  # pragma: no cover
    parser = get_parser()
    args = parser.parse_args()
    output, errors = main(**vars(args))
    if errors:
        parser.print_help()
        print("\nUnable to convert the Wordle, because:", file=sys.stderr)
        for error in errors:
            print(f"* {error}", file=sys.stderr)
        sys.exit(1)
    print(output)
