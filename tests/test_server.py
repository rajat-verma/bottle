import unittest
from unittest import mock
from io import BytesIO
import json

from bottle_bot import server


class ServerTests(unittest.TestCase):
    def make_handler(self, payload, event='issue_comment'):
        data = json.dumps(payload).encode('utf-8')
        handler = server.WebhookHandler.__new__(server.WebhookHandler)
        handler.rfile = BytesIO(data)
        handler.wfile = BytesIO()
        handler.headers = {
            'content-length': str(len(data)),
            'X-GitHub-Event': event
        }
        handler.send_response = lambda code: setattr(handler, 'response_code', code)
        handler.end_headers = lambda: None
        return handler

    def test_do_post_processes_comment(self):
        payload = {
            'comment': {'body': '@bottle help'},
            'issue': {'number': 1, 'pull_request': {'url': 'x'}}
        }
        handler = self.make_handler(payload)
        pr_info = {'title': 't'}
        with mock.patch.object(server.gh_client, 'get_pr', return_value=pr_info) as gp, \
             mock.patch.object(server, 'handle_comment', return_value='res') as hc, \
             mock.patch.object(server.gh_client, 'post_comment') as pc:
            server.WebhookHandler.do_POST(handler)
        gp.assert_called_with(1)
        hc.assert_called_with('@bottle help', pr_info)
        pc.assert_called_with(1, 'res')
        self.assertEqual(handler.response_code, 200)

    def test_run_starts_server(self):
        with mock.patch('bottle_bot.server.HTTPServer') as mock_server:
            server.run(1234)
            mock_server.assert_called_with(('', 1234), server.WebhookHandler)
            mock_server.return_value.serve_forever.assert_called_once()

