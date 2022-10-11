from typing import Protocol
from git import Repo, Head
from github import Github
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
        self._repo_path = repo_path
        self.repo = Repo(repo_path)

    @property
    def active_branch(self) -> Head:
        return self.repo.active_branch

    @property
    def repo_path(self) -> str:
        return self._repo_path

    @property
    def remote_repo_name(self) -> bool:
        return self.repo.remotes.origin.url.split('.git')[0].split(':')[1]

    @property
    def remote_repository(self) -> bool:
        return git_api.get_repo(self.remote_repo_name)

    def queue(self) -> str:
        original_branch_name = self.repo.active_branch.name

        if original_branch_name in ['main', 'master']:
            logger.error(
                "Can't merge from main/master", your_branch=original_branch_name
            )
            return
        jet_branch_name = f'jet-{self.repo.active_branch.name}-{self.repo.active_branch.commit}'

        self.fetch_remote_branches()

        self.stash_current_changes()

        self.checkout_branch(self.is_main_or_master())
        self.checkout_branch(jet_branch_name, '-b')

        try:            
            logger.info(
                "Starting Merge", jet_branch_name=jet_branch_name, original_branch_name=original_branch_name
            )
            self.merge_from_branch(original_branch_name)
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

        repo = self.remote_repository

        try:
            logger.info(
                "Creating pull request"
            )
            repo.create_pull(
                title=f'Jet-MR {jet_branch_name}',
                body='Jet-bot created this MR :)',
                head=jet_branch_name,
                base=self.is_main_or_master(),
            )
        except Exception as e:
            logger.exception(e)

        self.repo.git.checkout(original_branch_name)
        try:
            self.repo.git.stash('pop')
        except Exception as e:
            logger.warning(e)


    def jet_branch_exists(self, new_branch_name: str) -> bool:
        branch = next((branch for branch in self.repo.branches if branch.name == new_branch_name), None) 

        if not branch:
            return False

        return True

    def is_main_or_master(self):
        output = self._run_command(['branch', '-l', 'master', 'main'])
        return output.split(' ')[-1]
        
    def checkout_branch(self, branch_to_checkout: str, option: str = None) -> bool:
        self.repo.git.checkout(option, branch_to_checkout)

    def fetch_remote_branches(self) -> None:
        for remote in self.repo.remotes:
            remote.fetch()

    def stash_current_changes(self) -> None:
        self.repo.git.stash('push')

    def pop_stash(self) -> None:
        self.repo.git.stash('apply')

    def merge_from_branch(self, branch: str) -> None:
        self.repo.git.merge(branch)

    def check_conflicts(self) -> bool:
        # This gets the dictionary discussed above 
        unmerged_blobs = self.repo.index.unmerged_blobs()

        # We're really interested in the stage each blob is associated with.
        # So we'll iterate through all of the paths and the entries in each value
        # list, but we won't do anything with most of the values.
        for path in unmerged_blobs:
            list_of_blobs = unmerged_blobs[path]
            for (stage, blob) in list_of_blobs:
                # Now we can check each stage to see whether there were any conflicts
                if stage != 0:
                    return True
        

    def _run_command(self, cmd):
        process = subprocess.Popen(
            ["git"] + cmd,
            stdout=subprocess.PIPE,
            # stderr=subprocess.DEVNULL,
            cwd=self._repo_path
        )
        output = process.communicate()

        if process.returncode != 0:
            raise Exception(f"internal git error: {output}")

        return output[0].decode('utf-8').strip()
