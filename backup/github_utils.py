import requests

GITHUB_API_URL = "https://api.github.com"


def validate_github_user(username):
    return requests.get(f"{GITHUB_API_URL}/users/{username}")


def validate_github_repo(username, repo_name):
    return requests.get(f"{GITHUB_API_URL}/repos/{username}/{repo_name}")
