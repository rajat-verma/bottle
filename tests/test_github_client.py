import unittest
from unittest import mock

from bottle_bot.github import client


class GitHubClientTests(unittest.TestCase):
    def test_get_pr_returns_info(self):
        pr = client.get_pr(5)
        self.assertEqual(pr['number'], 5)
        self.assertIn('html_url', pr)

    def test_post_comment_prints(self):
        with mock.patch('builtins.print') as mock_print:
            client.post_comment(2, 'hi')
            mock_print.assert_called_with('Would post comment to PR 2: hi')

