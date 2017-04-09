import json

from ioutils import GitHub

def lambda_handler(event, context):
    querystring = event['params']['querystring']
    owner = querystring.get('owner')
    repo = querystring.get('repo')
    gh_api_token = querystring.get('gh_api_token')
    gh_query_params_string = querystring.get('gh_query_params')
    gh_query_params = (
        json.loads(gh_query_params_string) if gh_query_params_string else
        {}
    )
    n_issues = int(querystring.get('n_issues'))
    github_io = GitHub(gh_api_token)
    return github_io.get_random_issues(owner, repo, gh_query_params, n_issues)
