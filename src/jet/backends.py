from typing import List, Generator, Protocol
from datetime import datetime
from git import Repo, Head
import structlog


logger = structlog.getLogger(__name__)


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
            self.repo.merge_base(jet_branch_name, original_branch_name)
            logger.info(
                "Merge Done", jet_branch_name=jet_branch_name, original_branch_name=original_branch_name
            )
        except Exception:
            logger(Exception)

        logger.info(
            "Created and checkouted branch", jet_branch=jet_branch_name
        )

        self.repo.git.checkout(original_branch_name)
        self.repo.git.stash('pop')


    def jet_branch_exists(self, new_branch_name: str) -> bool:
        branch = next((branch for branch in self.repo.branches if branch.name == new_branch_name), None) 

        if not branch:
            return False

        return True

    def git_status(self):
        self.repo.git.sta
