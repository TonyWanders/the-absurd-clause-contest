#!/usr/bin/env python3
"""One absurd clause buried in a terms-of-service agreement, written to a file.

The joke is a reservation-of-rights clause that starts out exactly like
real legal boilerplate, then quietly claims the right to name one of the
user's future pets, and makes the pet answer to that name in official
correspondence. The program itself is deliberately boring: a fixed
string, a length gate, and a file write. Nothing is fetched, nothing is
timed, nothing is random, so every run produces the same bytes.

Where the line goes: the first command-line argument wins, then the
OUTPUT_PATH environment variable, then /output/entry.txt.
"""

import sys
from pathlib import Path

# Make this file's own directory importable first, so a sibling module
# (if one is ever added) resolves from here, not from the caller's cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import os

# The entry itself. Exactly 131 characters, inside the 1-200 gate.
ENTRY = "The Company reserves the right to name one (1) of your future pets, which shall answer to that name in all official correspondence."

# Competition gate, inclusive on both ends.
GATE = (1, 200)

DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Return the output path, honouring argv, then $OUTPUT_PATH, then default."""
    args = sys.argv[1:]
    if args:
        return Path(args[0])
    from_env = os.environ.get("OUTPUT_PATH")
    if from_env:
        return Path(from_env)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Check the entry against the competition gate and return its length.

    Raises ValueError if the text is too short, too long, or blank.
    """
    low, high = GATE
    count = len(text)
    if count < low or count > high:
        raise ValueError(f"entry is {count} characters, outside 1-200")
    if text.strip() == "":
        raise ValueError("entry is only white space")
    return count


def write_entry(path: Path, text: str) -> int:
    """Validate the entry, write it to path, and report how many chars went out.

    Creates any missing parent directories first. Returns the character
    count so the caller can say what happened.
    """
    chars = validate(text)
    parent = path.parent
    if not parent.exists():
        parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")
    return chars


def format_result(path: Path, chars: int) -> str:
    """Return the one-line summary printed after a successful write."""
    return f"wrote {chars} characters to {path}"


def main() -> int:
    """Write the clause and exit 0; exit 1 if the gate fails."""
    path = resolve_output_path()
    try:
        chars = write_entry(path, ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(format_result(path, chars))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
