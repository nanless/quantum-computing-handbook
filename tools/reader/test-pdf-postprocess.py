"""Regression tests for print font sampling across Chrome PDF font formats."""

import runpy
import unittest
from pathlib import Path


sample_line = runpy.run_path(str(Path(__file__).with_name("postprocess-pdf.py")))["prose_line_font_sizes"]


class ProseFontSamplingTests(unittest.TestCase):
    def test_character_spans_match_a_single_span(self):
        text = "复振幅需要先归一化"
        for size in (8.09, 9.49):
            with self.subTest(size=size):
                span = {"text": text, "size": size, "bbox": (45, 100, 135, 112)}
                split = [{**span, "text": character} for character in text]
                self.assertEqual(sample_line(split, 842), [size] * len(text))
                self.assertEqual(sample_line(split, 842), sample_line([span], 842))

    def test_excludes_running_header_and_short_labels(self):
        header = {"text": "量子计算手册", "size": 7.4, "bbox": (45, 22, 90, 31)}
        label = {"text": "图表", "size": 8.2, "bbox": (45, 100, 63, 112)}
        self.assertEqual(sample_line([header, label], 842), [])


if __name__ == "__main__":
    unittest.main()
