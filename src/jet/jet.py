import os
import structlog
from github import Github
from dotenv import load_dotenv
from jet.backends import GitBackend
load_dotenv()

logger = structlog.getLogger(__name__)
git_api = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))

def get_current_branch() -> str:
    logger.info(
        "Listing current branch for current git account",
    )
    git = GitBackend('.')
    return git.active_branch
    
def merge_with_origin_main():
    ...

def queue():
    ...

def create_branch():
    git = GitBackend('.')
    # Check if jet-branch already exists 
    jet_branch_name = f'jet-{git.active_branch.name}-{git.active_branch.commit}'

    if git.jet_branch_exists(jet_branch_name):
        logger.warning('Jet branch has already been created')
        return
    
    return git.create_branch()
