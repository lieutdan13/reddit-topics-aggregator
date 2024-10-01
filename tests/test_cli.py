import functools
from importlib.metadata import version
from types import FunctionType

import pytest
from click.testing import CliRunner

from reddit_topics_aggregator.cli import main

# See https://click.palletsprojects.com/testing/


@pytest.fixture
def cli() -> FunctionType:
    runner = CliRunner()
    yield functools.partial(runner.invoke, main)


def test_cli_output(cli: FunctionType):
    assert cli().output.rstrip() == "Hello, Reddit Topics Aggregator!"


def test_cli_version(cli: FunctionType):
    expected_version = version("reddit-topics-aggregator")
    assert cli(["--version"]).output.rstrip() == expected_version


def test_cli_reverse(cli: FunctionType):
    assert cli(["Foo"]).output.rstrip().endswith("ooF")


@pytest.mark.parametrize(
    "input_str,expected_output", [("Foo", "OOF"), ("Bar", "RAB")]
)
def test_cli_option_capitalize(cli: FunctionType, input_str, expected_output):
    assert (
        cli(["--capitalize", input_str])
        .output.rstrip()
        .endswith(expected_output)
    )
