import unittest
from unittest import mock

from bottle_bot.commands import cmr


class CMRCommandTests(unittest.TestCase):
    def test_run_creates_ticket_with_compressed_summary(self):
        pr_info = {
            'title': 'My Title',
            'body': 'x' * 60,
            'html_url': 'http://example.com/pr/1'
        }
        called = {}

        def fake_compress(text):
            called['compress_text'] = text
            return 'short'

        def fake_create_ticket(project_key, title, summary, pr_url):
            called['project_key'] = project_key
            called['title'] = title
            called['summary'] = summary
            called['pr_url'] = pr_url
            return {'key': 'PROJ-1', 'url': 'url'}

        with mock.patch.object(cmr.compressor, 'compress', fake_compress), \
             mock.patch.object(cmr.jira_client, 'create_ticket', fake_create_ticket):
            result = cmr.run(pr_info, ['PROJ'])

        self.assertEqual(called['compress_text'], pr_info['body'])
        self.assertEqual(called['project_key'], 'PROJ')
        self.assertEqual(called['title'], 'My Title')
        self.assertEqual(called['summary'], 'short')
        self.assertEqual(called['pr_url'], 'http://example.com/pr/1')
        self.assertEqual(result['key'], 'PROJ-1')

    def test_run_without_project_key_raises(self):
        with self.assertRaises(ValueError):
            cmr.run({}, [])

