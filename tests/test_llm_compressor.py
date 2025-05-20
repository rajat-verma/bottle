import unittest

from bottle_bot.llm import compressor


class CompressorTests(unittest.TestCase):
    def test_compress_truncates_to_50_chars(self):
        text = 'a' * 60
        self.assertEqual(compressor.compress(text), 'a' * 50)

