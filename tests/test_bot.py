import unittest
from unittest import mock

from bottle_bot import bot


class BotTests(unittest.TestCase):
    def test_parse_command(self):
        self.assertEqual(bot.parse_command('@bottle help'), ('help', []))
        self.assertIsNone(bot.parse_command('no command'))

    def test_help_command(self):
        pr_info = {}
        result = bot.handle_comment('@bottle help', pr_info)
        self.assertIn('Available commands', result)

    def test_cmr_command(self):
        pr_info = {
            'title': 'Add feature',
            'body': 'This adds a new feature',
            'html_url': 'https://github.com/example/repo/pull/1'
        }

        called = {}

        def fake_create_ticket(project_key, title, summary, pr_url):
            called['project_key'] = project_key
            called['title'] = title
            called['summary'] = summary
            called['pr_url'] = pr_url
            return {'key': 'PROJ-1', 'url': 'https://jira.example.com/browse/PROJ-1'}

        with mock.patch.object(bot.cmr.jira_client, 'create_ticket', fake_create_ticket):
            res = bot.handle_comment('@bottle CMR PROJ', pr_info)

        self.assertEqual(called['project_key'], 'PROJ')
        self.assertEqual(called['title'], 'Add feature')
        self.assertEqual(res['key'], 'PROJ-1')


if __name__ == '__main__':
    unittest.main()
