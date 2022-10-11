from jet.backends import GitBackend
from uuid import uuid4
import pytest
import tempfile
from pathlib import Path
import pytest
from github import Github
import git
import pytest


@pytest.fixture()
def git_setup():
    # Creates a brand new git repo
    with tempfile.TemporaryDirectory() as direct:
        git.Repo.init(path=Path(direct))
        git_repo = GitBackend(repo_path=Path(direct))
        open(Path(direct + "/new-file"), "wb").close()
        git_repo.repo.index.add(["new-file"])
        git_repo.repo.index.commit("initial commit")
        yield git_repo

def test_get_active_branch(git_setup):
    branch_name = git_setup.active_branch.name
    print(branch_name)
    assert branch_name == 'master'

def test_queue_from_main_or_master(git_setup):
    filename = str(git_setup.repo_path) + "/" + str(uuid4())
    open(filename, "wb").close()
    git_setup.repo.index.add([filename])
    git_setup.repo.index.commit("follow up file")
    git_setup.queue()

def test_queue_from_a_branch(git_setup):
    filename = str(git_setup.repo_path) + "/" + str(uuid4())
    open(filename, "wb").close()
    git_setup.repo.index.add([filename])
    git_setup.repo.index.commit("follow up file")
    git_setup.queue()

def test_queue_with_conflicts(git_setup):
    branch_name = git_setup.active_branch.name
    print(branch_name)
    assert branch_name == 'master'

def test_is_main_or_master(git_setup):
    branch_name = git_setup.is_main_or_master()
    assert branch_name == 'master'
