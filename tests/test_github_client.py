import unittest
from unittest import mock

from bottle_bot.github import client


class GitHubClientTests(unittest.TestCase):
    def test_get_pr_calls_api(self):
        fake_resp = mock.Mock()
        fake_resp.json.return_value = {'number': 5}
        fake_resp.raise_for_status = mock.Mock()
        with mock.patch.object(client, 'REPO', 'own/repo'):
            with mock.patch.object(client.session, 'get', return_value=fake_resp) as mget:
                pr = client.get_pr(5)
        mget.assert_called_with('https://api.github.com/repos/own/repo/pulls/5')
        fake_resp.raise_for_status.assert_called_once()
        self.assertEqual(pr['number'], 5)

    def test_post_comment_calls_api(self):
        fake_resp = mock.Mock()
        fake_resp.raise_for_status = mock.Mock()
        with mock.patch.object(client, 'REPO', 'own/repo'):
            with mock.patch.object(client.session, 'post', return_value=fake_resp) as mpost:
                client.post_comment(2, 'hi')
        mpost.assert_called_with('https://api.github.com/repos/own/repo/issues/2/comments',
                                 json={'body': 'hi'})
        fake_resp.raise_for_status.assert_called_once()

