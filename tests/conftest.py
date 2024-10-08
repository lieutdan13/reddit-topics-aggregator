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
    os.environ.pop("REDDIT_CLIENT_ID", None)
    os.environ.pop("REDDIT_CLIENT_SECRET", None)
    os.environ.pop("REDDIT_USERNAME", None)
    os.environ.pop("REDDIT_PASSWORD", None)
    os.environ.pop("REDDIT_USER_AGENT", None)
