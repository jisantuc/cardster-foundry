import re
import requests

from ioutils import GitHub

def lambda_handler(event, context):
    owner = event.get('owner')
    repo = event.get('repo')
    gh_api_token = event.get('gh_api_token')
    gh_query_params = event.get('gh_query_params')
    github_io = GitHub(gh_api_token)
    return github_io.get_all_issues(owner, repo, gh_query_params)
