"""Tests for converdle.py"""
from io import StringIO
from unittest import mock

import pytest

from converdle import get_parser, main

EMOJI_WORDLE = """
Wordle 222 3/6

⬛🟨⬛⬛🟩
⬛🟩⬛🟩🟩
🟩🟩🟩🟩🟩
"""


def test_main_from_inputfile():
    result, errors = main(inputfile=StringIO(EMOJI_WORDLE), replace="ABC")
    assert result is not None
    assert errors == []


def test_main_with_components():
    result, errors = main(
        inputfile=StringIO(EMOJI_WORDLE), miss=" ", wrong="x", right="✓"
    )
    assert result is not None
    assert errors == []


def test_main_fails_stdin_tty():
    fake_stdin = mock.Mock(spec_set=["isatty", "read"])
    fake_stdin.isatty.return_value = True
    fake_stdin.read.side_effect = Exception("Not Called")
    result, errors = main(inputfile=fake_stdin, replace="ABC")
    assert result is None
    assert errors == ["Must specify an inputfile or pipe the input"]


def test_main_fails_components_and_replace():
    result, errors = main(
        inputfile=StringIO(EMOJI_WORDLE), miss=" ", wrong="x", right="✓", replace="ABC"
    )
    assert result is None
    assert errors == [
        "Can not use --miss and --replace",
        "Can not use --wrong and --replace",
        "Can not use --right and --replace",
    ]


def test_main_fails_no_components_or_replace():
    result, errors = main(inputfile=StringIO(EMOJI_WORDLE))
    assert result is None
    assert errors == [
        "Must specify replacements with --replace or --miss, --wrong, and --right"
    ]


def test_main_fails_bad_replace():
    result, errors = main(inputfile=StringIO(EMOJI_WORDLE), replace="X")
    assert result is None
    assert errors == ["Unable to parse --replace"]


@pytest.mark.parametrize("component", ("miss", "wrong", "right"))
def test_main_fails_bad_component(component):
    components = {
        "miss": " ",
        "wrong": "x",
        "right": "y",
    }
    components[component] = "an invalid string"
    result, errors = main(inputfile=StringIO(EMOJI_WORDLE), **components)
    assert result is None
    assert errors == [f"Unable to parse -{component[0]}/--{component}"]


@pytest.mark.parametrize("component", ("miss", "wrong", "right"))
def test_main_fails_missing_component(component):
    components = {
        "miss": " ",
        "wrong": "x",
        "right": "y",
    }
    del components[component]
    result, errors = main(inputfile=StringIO(EMOJI_WORDLE), **components)
    assert result is None
    assert errors == [f"Must specify -{component[0]}/--{component}"]


def test_get_parser():
    parser = get_parser()
    args = parser.parse_args(["--replace", "ABC"])
    assert args.inputfile is None
    assert args.replace == "ABC"
    assert args.miss is None
