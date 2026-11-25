#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun entry.

Writes a single line of quiet, earned pride to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set). Deterministic, no network.
"""
import os
import sys

LINE = ("After six weeks of evening practice, my father stood at the wedding, "
        "unfolded his shaking hands, and read his whole speech out loud "
        "without looking down once.")


def main() -> int:
    if not (1 <= len(LINE) <= 240):
        print(f"line is {len(LINE)} chars, must be 1-240", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("line is only whitespace", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("line must be a single line", file=sys.stderr)
        return 1
    if any(ord(c) < 32 and c not in "\t" for c in LINE) or "\t" in LINE:
        print("line must not contain control characters", file=sys.stderr)
        return 1
    try:
        LINE.encode("utf-8")
    except UnicodeEncodeError:
        print("line must be valid UTF-8 text", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    # Read back and verify what was written is exactly the line.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LINE:
        print("read-back mismatch", file=sys.stderr)
        return 1
    print(f"wrote {len(LINE)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
