"""Shared helpers for the site tests. Standard library only."""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def read(rel: str) -> str:
    """Return the text of a file given relative to the repo root."""
    return (ROOT / rel).read_text(encoding="utf-8")


def front_matter(rel: str) -> dict:
    """Parse the leading --- ... --- block as simple `key: value` lines.

    Only the block at the very top of the file is read. Surrounding quotes
    are stripped from values. Anything that is not `key: value` is skipped.
    """
    lines = read(rel).splitlines()
    result = {}
    if not lines or lines[0].strip() != "---":
        return result
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^\s*([A-Za-z_][\w-]*)\s*:\s*(.*?)\s*$", line)
        if not m:
            continue
        value = m.group(2)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        result[m.group(1)] = value
    return result


def _channel(c: int) -> float:
    s = c / 255.0
    if s <= 0.03928:
        return s / 12.92
    return ((s + 0.055) / 1.055) ** 2.4


def _luminance(hex_color: str) -> float:
    h = hex_color.strip().lstrip("#")
    if len(h) != 6:
        raise ValueError(f"expected #RRGGBB, got {hex_color!r}")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast(hex1: str, hex2: str) -> float:
    """WCAG 2.x contrast ratio between two #RRGGBB colours (1.0 to 21.0)."""
    l1, l2 = _luminance(hex1), _luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)
