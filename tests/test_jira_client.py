import unittest

from bottle_bot.jira import client


class JiraClientTests(unittest.TestCase):
    def test_create_ticket(self):
        ticket = client.create_ticket('PROJ', 'Title', 'Summary', 'url')
        self.assertEqual(ticket['key'], 'PROJ-123')
        self.assertIn('PROJ-123', ticket['url'])

