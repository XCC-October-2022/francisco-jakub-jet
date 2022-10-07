from typing import Protocol
from git import Repo, Head
from github import Github
from dotenv import load_dotenv
import subprocess
import structlog
import os

logger = structlog.getLogger(__name__)
git_api = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))

class Backend(Protocol):
    def create_branch(self) -> str:
        ...


class GitBackend:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

    @property
    def active_branch(self) -> Head:
        return self.repo.active_branch

    def create_branch(self) -> str:
        repo_name = self.repo.remotes.origin.url.split('.git')[0].split(':')[1]
        original_branch_name = self.repo.active_branch.name
        jet_branch_name = f'jet-{self.repo.active_branch.name}-{self.repo.active_branch.commit}'

        for remote in self.repo.remotes:
            remote.fetch()

        self.repo.git.stash('push')
        logger.info(
            "Stashing uncommited changes on current branch", current_branch=original_branch_name
        )

        self.repo.git.checkout('main')

        self.repo.git.checkout('-b', jet_branch_name)

        try:            
            logger.info(
                "Starting Merge", jet_branch_name=jet_branch_name, original_branch_name=original_branch_name
            )
            self.repo.git.merge(original_branch_name)
            logger.info(
                "Merge Done", jet_branch_name=jet_branch_name, original_branch_name=original_branch_name
            )
        except Exception:
            logger(Exception)

        push_command= f'git push origin {jet_branch_name}'
        p = subprocess.Popen(push_command.split())
        p.communicate()
        logger.info(
            "Pushing branch", jet_branch_name=jet_branch_name
        )

        try:
            repo = git_api.get_repo(repo_name)
        except Exception:
            print(Exception)

        try:
            logger.info(
                "Creating pull request"
            )
            repo.create_pull(
                title=f'Jet-MR {self.repo.active_branch.name}',
                body='Jet-bot created this MR :)',
                head=jet_branch_name,
                base='main' 
            )
        except Exception as e:
            logger.exception(e)

        self.repo.git.checkout(original_branch_name)
        self.repo.git.stash('pop')


    def jet_branch_exists(self, new_branch_name: str) -> bool:
        branch = next((branch for branch in self.repo.branches if branch.name == new_branch_name), None) 

        if not branch:
            return False

        return True

    def git_status(self):
        self.repo.git.sta
