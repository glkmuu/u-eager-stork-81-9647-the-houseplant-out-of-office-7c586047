#!/usr/bin/env python3
"""Houseplant out-of-office entry writer.

Writes the fixed one-line entry (92 characters, at most 120 per the
competition gate) to /output/entry.txt for grading and to entry.txt
beside this script for inspection. Stdlib only; the entry text is a
constant and is never generated, edited, or read from anywhere else,
so every run produces byte-identical output.
"""

import os

ENTRY = "Out of office: I'm the fern. Nobody has watered me in months. Your email has been composted."

OUTPUT_PATH = "/output/entry.txt"


def validate_entry(entry):
    """Gate check: entry must be a UTF-8 string of 1-120 characters,
    exactly one line, and not only whitespace.

    Raises a specific error naming the failed check so a bad entry
    can be diagnosed without guessing which rule it broke.
    """
    if not isinstance(entry, str):
        raise TypeError("entry must be a str, got %s" % type(entry).__name__)
    if not entry.strip():
        raise ValueError("entry is empty or only whitespace: nothing to submit")
    if len(entry) > 120:
        raise ValueError(
            "entry is %d characters, %d over the 120-character limit"
            % (len(entry), len(entry) - 120))
    if "\n" in entry or "\r" in entry:
        raise ValueError(
            "entry must be a single line, but contains a line break "
            "(%d characters)" % len(entry))
    try:
        entry.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("entry is not valid UTF-8 text: %s" % exc) from exc
    return True


def write_and_verify(path, data):
    """Write bytes to path, read them back, fail hard on any mismatch."""
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        raise RuntimeError("verify failed for %s: wrote %d bytes, read back %d bytes"
                           % (path, len(data), len(back)))
    return len(back)


def main():
    validate_entry(ENTRY)
    here = os.path.dirname(os.path.abspath(__file__))
    targets = [OUTPUT_PATH, os.path.join(here, "entry.txt")]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    data = ENTRY.encode("utf-8")
    written = {}
    for path in targets:
        written[path] = write_and_verify(path, data)

    print("Wrote %d bytes to %s (verified)"
          % (written[OUTPUT_PATH], ", ".join(targets)))


if __name__ == "__main__":
    main()
