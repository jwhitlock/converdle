# Converdle - Convert a Wordle to a new format

This converts the result text from
[Wordle](https://www.powerlanguage.co.uk/wordle/)
to a different form.

## Installation
Requires Python 3. I used Python 3.9, but an earlier version may work.

## Usage:

Using the example file:

```sh
> cat wordle_example.txt 
Wordle 222 3/6

⬛🟨⬛⬛🟩
⬛🟩⬛🟩🟩
🟩🟩🟩🟩🟩

> ./converdle.py wordle_example.txt --replace ⚫️🟡🟢
Wordle 222 3/6

⚫🟡⚫⚫🟢
⚫🟢⚫🟢🟢
🟢🟢🟢🟢🟢

> ./converdle.py wordle_example.txt --replace 👎👋👍
Wordle 222 3/6

👎👋👎👎👍
👎👍👎👍👍
👍👍👍👍👍

> ./converdle.py --help
usage: Convert the wordle to something different [-h] [-m MISS] [-w WRONG] [-r RIGHT] [--replace REPLACE] [inputfile]

positional arguments:
  inputfile             An input file with a Wordle result. Alternatively, pipe the text to the program.

optional arguments:
  -h, --help            show this help message and exit
  -m MISS, --miss MISS  The replacement for ⬛, a missed letter
  -w WRONG, --wrong WRONG
                        The replacement for 🟨, a matching letter in the wrong place
  -r RIGHT, --right RIGHT
                        The replacement for 🟩, a matching letter in the right place
  --replace REPLACE     The three replacements, in ⬛🟨🟩 order
```

