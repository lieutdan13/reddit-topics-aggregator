import functools
from collections.abc import Generator
from types import FunctionType

import pytest
from click.testing import CliRunner

from reddit_topics_aggregator.cli import reddit_topics_aggregator


@pytest.fixture(scope="module")
def cli() -> Generator[FunctionType]:
    runner = CliRunner()
    yield functools.partial(runner.invoke, reddit_topics_aggregator)
