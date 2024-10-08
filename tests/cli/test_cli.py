from importlib.metadata import version
from types import FunctionType


def test_cli_output(cli: FunctionType):
    result = cli()
    assert result.exit_code == 0
    assert result.output.rstrip().startswith("Usage: ")


def test_cli_version(cli: FunctionType):
    expected_version = version("reddit-topics-aggregator")
    result = cli(["--version"])
    assert result.exit_code == 0
    assert result.output.rstrip() == expected_version
