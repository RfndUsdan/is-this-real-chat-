"""Shared deterministic text helpers used by validation, dedup, and split.

These helpers contain no learned state. They are deliberately small so that
the same rules can be reused by training and inference later.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable, Sequence

UNICODE_FORM = "NFKC"
TOKEN_SEPARATOR = re.compile(r"[^a-z0-9\u00c0-\u024f]+")
ALLOWED_CONTROL_CHARS = frozenset({"\t", "\n", "\r"})


def normalize_unicode(text: str, form: str = UNICODE_FORM) -> str:
    """Normalize Unicode using a fixed, reproducible normalization form."""
    return unicodedata.normalize(form, text)


def normalize_whitespace(text: str) -> str:
    """Collapse all Unicode whitespace runs into a single ASCII space."""
    return " ".join(text.split())


def normalize_for_comparison(text: str) -> str:
    """Return a canonical comparison key without altering stored raw text."""
    return normalize_whitespace(normalize_unicode(text))


def has_invalid_control_chars(text: str) -> bool:
    """Detect control characters other than tab, LF, and CR."""
    return any(
        unicodedata.category(char) == "Cc" and char not in ALLOWED_CONTROL_CHARS
        for char in text
    )


def alphanumeric_tokens(text: str) -> list[str]:
    """Casefold and tokenize while keeping Indonesian letters and digits."""
    normalized = normalize_for_comparison(text).casefold()
    cleaned = TOKEN_SEPARATOR.sub(" ", normalized).strip()
    return cleaned.split() if cleaned else []


def word_shingles(tokens: Sequence[str] | Iterable[str], size: int) -> set[tuple[str, ...]]:
    """Build a set of contiguous word shingles of fixed size."""
    if size < 1:
        raise ValueError("shingle size must be at least 1")
    token_list = list(tokens)
    if len(token_list) < size:
        return set()
    return {
        tuple(token_list[index : index + size])
        for index in range(len(token_list) - size + 1)
    }


def jaccard(left: set[tuple[str, ...]], right: set[tuple[str, ...]]) -> float:
    """Return Jaccard similarity; disjoint or empty sets score zero."""
    if not left or not right:
        return 0.0
    union = left | right
    return len(left & right) / len(union)
