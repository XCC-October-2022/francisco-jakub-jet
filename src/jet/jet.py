import structlog
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

logger = structlog.getLogger(__name__)
git_api = Github('key')


def list_repos(roman_number: str) -> int:
    for repo in g.get_user().get_repos():
        print(repo.name)

