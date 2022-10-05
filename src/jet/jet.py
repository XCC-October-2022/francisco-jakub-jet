import structlog
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

logger = structlog.getLogger(__name__)
git_api = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))

def list_repos(test: int):
    logger.info(
        "Listing repositories for current git account",
    )
    for repo in git_api.get_user().get_repos():
        print(repo.name)
