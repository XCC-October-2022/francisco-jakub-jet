import structlog
from github import Github
from pygit2 import Repository, GIT_STATUS_CURRENT
from dotenv import load_dotenv
import os

load_dotenv()

logger = structlog.getLogger(__name__)
git_api = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))
repo = Repository('.')

def list_repos():
    logger.info(
        "Listing repositories for current git account",
    )
    return git_api.get_user().get_repos()


def get_current_branch() -> str:
    logger.info(
        "Listing current branch for current git account",
    )

    status = repo.status()
    for filepath, flags in status.items():
        if flags != GIT_STATUS_CURRENT:
            flag = True
            logger.warning(
                "Current branch contains untracked changed.", filepath=filepath
            )
    if flag:
        #repo.stash(repo.default_signature, "Jet-Stashing: untracked changes.")
        ...
    for stash in repo.listall_stashes():
        print(stash)
    return repo.head.shorthand

def add_to_queue(commit: str, force: bool = False):
    logger.info(
        "Running add_to_queue with commit message {commit}",
    )
    branch_name = repo.head.shorthand
    new_branch = repo.create_branch(f'jet-{branch_name}', commit, force)

    status = repo.status()
    for filepath, flags in status.items():
        if flags != GIT_STATUS_CURRENT:
            flag = True
            logger.warning(
                "Current branch contains untracked changed.", filepath=filepath
            )
    if flag:
        repo.stash(repo.default_signature, "Jet-Stashing: untracked changes.")

    repo.checkout(new_branch.branch_name)

    repo.merge(repo.branches.get('origin-main').branch_name)
    
    repo.stash_pop()
        

