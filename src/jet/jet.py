import structlog
from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

logger = structlog.getLogger(__name__)
git_api = Github('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')


def list_repos(roman_number: str) -> int:
    ...
