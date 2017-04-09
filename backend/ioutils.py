import random
import re
import requests

class GitHub(object):
    def __init__(self, token=None):
        self.token = token
        self.headers = (
            {'Authorization': 'Token ' + self.token} if self.token else None
        )

    @staticmethod
    def get_next(response):
        has_next = (
            response.headers.get('Link') and 'rel="next"' in
            response.headers['Link']
        )
        if has_next:
            link = response.headers['Link']
            match = re.match(r'\<(.*)\>;.*rel="next".*', link)
            assert match.groups(), 'No match found'
            uri = match.groups()[0] if match.groups() else None
        else:
            uri = None
        return uri

    @staticmethod
    def trim_issues(issues):
        return [{'title': issue['title'],
                 'body': issue['body'],
                 'labels': issue['labels'],
                 'number': issue['number']} for issue in issues]

    def get_all_issues(self, owner, repo, query_params):
        uri = 'https://api.github.com/repos/{owner}/{repo}/issues'.format(
            owner=owner, repo=repo
        )
        query_params.update({'is': 'open'})
        resp = requests.get(
            uri,
            headers=self.headers,
            params=query_params
        )
        resp.raise_for_status()

        issues = resp.json()

        has_next = self.get_next(resp)
        page = 1
        while has_next:
            page += 1
            query_params.update({'page': page})
            resp = requests.get(uri, headers=self.headers, params=query_params)
            resp.raise_for_status()
            issues = issues + resp.json()
            has_next = self.get_next(resp)
        return self.trim_issues(issues)

    def get_random_issues(self, owner, repo, query_params, n_issues=2):
        all_issues = self.get_all_issues(owner, repo, query_params)
        return sorted(all_issues, key=lambda x: random.random())[:n_issues]
