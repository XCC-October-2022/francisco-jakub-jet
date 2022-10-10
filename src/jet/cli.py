from typer import Typer
from jet import jet
import sys
import logging

app = Typer()
logger = logging.Logger(__name__)

@app.command()
def list_repos():
    repos = jet.list_repos()
    for repo in repos:
        print(repo.name)

@app.command()
def get_current_branch():
    print(jet.get_current_branch())

@app.command()
def queue(commit_message: str):
    jet.add_to_queue(commit_message)

@app.command()
def test_branch():
    jet.create_branch()

def main():
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('jet').setLevel(logging.INFO)
    logging.getLogger('jet.jet').setLevel(logging.DEBUG)

    app()


if __name__ == "__main__":
    main()
