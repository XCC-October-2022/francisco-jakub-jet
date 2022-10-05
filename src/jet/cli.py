from typer import Typer
from jet import jet
import sys
import logging

app = Typer()

@app.command
def list_repos():
    print(jet.list_repos())


def main():
    app()


if __name__ == "__main__":
    main()
