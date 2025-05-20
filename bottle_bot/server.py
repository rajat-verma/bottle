import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .bot import handle_comment
from .github import client as gh_client


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length)
        event = self.headers.get('X-GitHub-Event', '')
        try:
            payload = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        if event == 'issue_comment':
            comment = payload.get('comment', {}).get('body', '')
            pr_data = payload.get('issue', {})
            if comment and pr_data.get('pull_request'):
                pr_number = pr_data.get('number')
                pr_info = gh_client.get_pr(pr_number)
                result = handle_comment(comment, pr_info)
                if result:
                    gh_client.post_comment(pr_number, str(result))

        self.send_response(200)
        self.end_headers()


def run(port: int = 8000):
    httpd = HTTPServer(("", port), WebhookHandler)
    print(f"Serving on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
