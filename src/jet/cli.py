from typer import Typer
from jet import jet
import sys
import logging

app = Typer()
logger = logging.Logger(__name__)

@app.command()
def list_repos(test: int):
    print(jet.list_repos(test))

@app.command()
def test(test: int):
    ...



def main():
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger('jet').setLevel(logging.INFO)
    logging.getLogger('jet.jet').setLevel(logging.DEBUG)

    app()


if __name__ == "__main__":
    main()
