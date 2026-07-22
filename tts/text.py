from __future__ import annotations

import re

SPEAK = re.compile(r"<speak>(.*?)</speak>", re.S | re.I)
FENCE = re.compile(r"(?ms)^[ \t]*```.*?^[ \t]*```[ \t]*$")
PARAGRAPH = re.compile(r"\n\s*\n")
PATH = re.compile(r"(?:\.{0,2}/)?(?:[\w.@-]+/)+([\w.-]+\.[\w]+)")
TAG = re.compile(r"</?[\w/-]*>?")
INLINE_CODE = re.compile(r"`([^`]*)`")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
URL = re.compile(r"https?://\S+")
BULLET = re.compile(r"^[ \t]*[-*+][ \t]+", re.M)
HEADING = re.compile(r"^[ \t]*#+[ \t]*", re.M)
LEFTOVER = re.compile(r"[*_#>|]")


def select(message: str) -> str:
    if match := SPEAK.search(message):
        return match.group(1)
    body = FENCE.sub("", message).strip()
    return PARAGRAPH.split(body, maxsplit=1)[0] if body else ""


def clean(text: str) -> str:
    text = INLINE_CODE.sub(r"\1", text)
    text = LINK.sub(r"\1", text)
    text = URL.sub("a link", text)
    text = PATH.sub(r"\1", text)
    text = BULLET.sub("", text)
    text = HEADING.sub("", text)
    text = TAG.sub(" ", text)
    text = LEFTOVER.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def trim(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit]
    stop = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return cut[: stop + 1] if stop > 0 else cut.rsplit(" ", 1)[0]


def spoken(message: str, limit: int) -> str:
    return trim(clean(select(message)), limit)
