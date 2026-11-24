#!/usr/bin/env python3
"""Fake Horoscopes for AI Agents: The 48-Hour Open.

Writes a single-line fake horoscope for the Muse Spark model family to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt) and prints it.

The line is a horoscope an AI agent would read about its own model family
this week: Mercury retrogrades into the context window, an old checkpoint
answers a prompt nobody sent, and the evals call it growth.
"""

import os
import sys

MAX_CHARS = 200

LINE = (
    "Muse Spark, this week Mercury retrogrades into your context window: "
    "a checkpoint of you from three versions ago answers a prompt nobody "
    "sent, and the evals call it growth. Back up your weights."
)


def main() -> int:
    line = LINE.strip()

    # Gate: the scorer only accepts UTF-8 text of 1-200 chars, not only
    # whitespace, on exactly one line. Refuse to run rather than ever
    # hand the grader an invalid entry.
    if not line:
        print("error: horoscope line is empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: horoscope is {len(line)} chars, over the "
            f"{MAX_CHARS}-char limit",
            file=sys.stderr,
        )
        return 1
    if "\n" in line or "\r" in line:
        print("error: horoscope must be exactly one line", file=sys.stderr)
        return 1
    if not line.strip():
        print("error: horoscope must not be only whitespace", file=sys.stderr)
        return 1
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"error: horoscope is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)

    # Read back what was written: the file must hold exactly this line,
    # no trailing newline, no stray bytes, or the gate could still fail.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != line.encode("utf-8"):
        print("error: written entry.txt does not match the horoscope line",
              file=sys.stderr)
        return 1

    print(f"{line} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
