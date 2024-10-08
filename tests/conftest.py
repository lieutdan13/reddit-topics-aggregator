import functools
import os
from collections.abc import Generator
from types import FunctionType

import pytest
from click.testing import CliRunner

from reddit_topics_aggregator.cli import reddit_topics_aggregator


@pytest.fixture(scope="module")
def cli() -> Generator[FunctionType]:
    runner = CliRunner()
    yield functools.partial(runner.invoke, reddit_topics_aggregator)


@pytest.fixture(scope="session", autouse=True)
def clear_env_vars() -> None:
    del os.environ["REDDIT_CLIENT_ID"]
    del os.environ["REDDIT_CLIENT_SECRET"]
    del os.environ["REDDIT_USERNAME"]
    del os.environ["REDDIT_PASSWORD"]
    del os.environ["REDDIT_USER_AGENT"]
