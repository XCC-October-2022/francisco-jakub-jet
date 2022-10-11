from jet.backends import GitBackend
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
