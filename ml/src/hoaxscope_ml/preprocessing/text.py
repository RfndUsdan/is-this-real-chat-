"""Modular, deterministic text preprocessing.

Each transformation is independent and configurable. No stemming, stopword
removal, or other information-destroying step is enabled by default.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Literal

from ..data.schema import CanonicalRecord
from ..text import normalize_unicode, normalize_whitespace

HTML_TAG = re.compile(r"<[^>]+>")
URL = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
TOKEN = re.compile(r"[\w]+", flags=re.UNICODE)

UrlPolicy = Literal["placeholder", "remove", "keep"]


@dataclass(frozen=True, slots=True)
class PreprocessingConfig:
    """Configuration for reproducible preprocessing.

    Defaults preserve negation, numbers, sentence order, and casing.
    """

    unicode_form: str = "NFKC"
    strip_html: bool = True
    url_policy: UrlPolicy = "placeholder"
    collapse_whitespace: bool = True
    lowercase: bool = False
    tokenize: bool = False

    def report_dict(self) -> dict[str, object]:
        return {
            "unicode_form": self.unicode_form,
            "strip_html": self.strip_html,
            "url_policy": self.url_policy,
            "collapse_whitespace": self.collapse_whitespace,
            "lowercase": self.lowercase,
            "tokenize": self.tokenize,
            "stemming": False,
            "stopword_removal": False,
        }


@dataclass(frozen=True, slots=True)
class PreprocessedRecord:
    """A derived representation; raw source text remains on the record."""

    record_id: str
    text: str
    tokens: tuple[str, ...] = ()

    def report_dict(self) -> dict[str, object]:
        return {
            "record_id": self.record_id,
            "text_length": len(self.text),
            "token_count": len(self.tokens),
        }


class TextPreprocessor:
    """Apply configured preprocessing steps in a fixed order."""

    def __init__(self, config: PreprocessingConfig | None = None) -> None:
        self.config = config or PreprocessingConfig()

    def clean_html(self, text: str) -> str:
        """Remove HTML tags and unescape entities."""
        return html.unescape(HTML_TAG.sub(" ", text))

    def handle_urls(self, text: str) -> str:
        """Replace, remove, or keep URLs according to the configured policy."""
        if self.config.url_policy == "keep":
            return text
        replacement = " URL " if self.config.url_policy == "placeholder" else " "
        return URL.sub(replacement, text)

    def transform_text(self, text: str) -> str:
        """Return the normalized text representation without tokenizing."""
        result = normalize_unicode(text, form=self.config.unicode_form)
        if self.config.strip_html:
            result = self.clean_html(result)
        result = self.handle_urls(result)
        if self.config.lowercase:
            result = result.casefold()
        if self.config.collapse_whitespace:
            result = normalize_whitespace(result)
        return result.strip()

    def tokenize(self, text: str) -> tuple[str, ...]:
        """Optional whitespace-safe tokenization preserving numbers and words."""
        return tuple(TOKEN.findall(text))

    def transform(self, record_id: str, text: str) -> PreprocessedRecord:
        """Preprocess one record and optionally produce tokens."""
        processed = self.transform_text(text)
        tokens = self.tokenize(processed) if self.config.tokenize else ()
        return PreprocessedRecord(record_id=record_id, text=processed, tokens=tokens)

    def transform_records(
        self, records: list[object]
    ) -> list[PreprocessedRecord]:
        """Preprocess canonical records without mutating their raw text."""
        return [
            self.transform(record.record_id, record.text)  # type: ignore[attr-defined]
            for record in records
        ]
