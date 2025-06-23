# tests/test_parser.py

import unittest
from dna_parser import parser

class TestParser(unittest.TestCase):
    def test_is_valid_dna(self):
        self.assertTrue(parser.is_valid_dna("ACGT"))
        self.assertFalse(parser.is_valid_dna("ACGTX"))

    def test_count_bases(self):
        counts = parser.count_bases("AAGCTT")
        self.assertEqual(counts, {"A": 2, "C": 1, "G": 1, "T": 2})

    def test_gc_content(self):
        self.assertAlmostEqual(parser.gc_content("GGCC"), 100.0)
        self.assertAlmostEqual(parser.gc_content("AATT"), 0.0)
        self.assertAlmostEqual(parser.gc_content("AGCT"), 50.0)

    def test_parse_dna(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write(">header\nACGT\nTGCA\n")
            f.flush()
            seq = parser.parse_dna(f.name)
        self.assertEqual(seq, "ACGTTGCA")

if __name__ == '__main__':
    unittest.main()