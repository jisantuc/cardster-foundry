import re
import requests


def get_next(response):
    has_next = response.headers.get('Link') and 'rel="next"' in response.headers['Link']
    if has_next:
        link = response.headers['Link']
        match = re.match(r'\<(.*)\>;.*rel="next".*', link)
        assert match.groups(), 'No match found'
        uri = match.groups()[0] if match.groups() else None
    else:
        uri = None
    return uri


def get_issues(event):
    github_token = event.get('github_api_token')
    owner = event.get('owner')
    repo = event.get('repo')
    headers = {'Authorization': 'Token ' + github_token} if github_token else {}
    params = {'per_page': 100}
    if event.get('issue_query_params'):
        params.update(event['issue_query_params'])
    resp = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/issues'.format(
            owner=owner, repo=repo
        ),
        headers=headers,
        params=params
    )
    resp.raise_for_status()

    issues = resp.json()

    has_next = get_next(resp)
    while has_next:
        resp = requests.get(has_next, headers=headers)
        resp.raise_for_status()
        issues = issues + resp.json()
        has_next = get_next(resp)
    return issues

def trim_issues(issues):
    return [issue['title'] for issue in issues]

def lambda_handler(event, context):
    issues = get_issues(event)
    trimmed = trim_issues(issues)
    return trimmed
