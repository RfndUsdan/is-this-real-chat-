"""Preprocessing tests using synthetic text only."""

from __future__ import annotations

import unittest

import helpers  # noqa: F401

from hoaxscope_ml.preprocessing.text import PreprocessingConfig, TextPreprocessor


class PreprocessingTests(unittest.TestCase):
    def test_default_preserves_negation_numbers_and_case(self) -> None:
        processor = TextPreprocessor()
        result = processor.transform("r1", "TIDAK Hoax 2026")
        self.assertEqual(result.text, "TIDAK Hoax 2026")

    def test_html_url_unicode_and_whitespace(self) -> None:
        processor = TextPreprocessor()
        result = processor.transform(
            "r1",
            "<p>ＡＢＣ　tidak   hoax　123</p> https://example.invalid/x",
        )
        self.assertEqual(result.text, "ABC tidak hoax 123 URL")

    def test_lowercase_and_tokenization_are_optional(self) -> None:
        default = TextPreprocessor().transform("r1", "TIDAK hoax 123")
        self.assertEqual(default.tokens, ())

        configured = TextPreprocessor(
            PreprocessingConfig(lowercase=True, tokenize=True)
        ).transform("r1", "TIDAK hoax 123")
        self.assertEqual(configured.text, "tidak hoax 123")
        self.assertEqual(configured.tokens, ("tidak", "hoax", "123"))

    def test_no_automatic_stemming_or_stopword_removal(self) -> None:
        config = PreprocessingConfig().report_dict()
        self.assertFalse(config["stemming"])
        self.assertFalse(config["stopword_removal"])


if __name__ == "__main__":
    unittest.main()
