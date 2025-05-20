import unittest

from bottle_bot.commands import help


class HelpCommandTests(unittest.TestCase):
    def test_run_returns_help_text(self):
        result = help.run({}, [])
        self.assertIn('CMR', result)

