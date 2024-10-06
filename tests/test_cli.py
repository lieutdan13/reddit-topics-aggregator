import functools
from collections.abc import Generator
from importlib.metadata import version
from types import FunctionType
from unittest.mock import MagicMock, patch

import praw.exceptions
import pytest
from click.testing import CliRunner

from reddit_topics_aggregator.cli import reddit_topics_aggregator

# See https://click.palletsprojects.com/testing/


@pytest.fixture
def cli() -> Generator[FunctionType]:
    runner = CliRunner()
    yield functools.partial(runner.invoke, reddit_topics_aggregator)


def test_cli_output(cli: FunctionType):
    result = cli()
    assert result.exit_code == 0
    assert result.output.rstrip().startswith("Usage: ")


def test_cli_version(cli: FunctionType):
    expected_version = version("reddit-topics-aggregator")
    result = cli(["--version"])
    assert result.exit_code == 0
    assert result.output.rstrip() == expected_version


def test_cli_connect(cli: FunctionType):
    result = cli(["connect"])
    assert result.exit_code != 0
    assert (
        "Configuration Error: Missing arguments: --client-id, --client-secret, --username, --password"
    ) in result.output
    assert (
        "Error: Help: Specify the arguments above and try again"
    ) in result.output


def test_cli_connect_401_authentication_error(cli: FunctionType):
    result = cli(
        [
            "connect",
            "--client-id",
            "test_id",
            "--client-secret",
            "test_secret",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )
    assert result.exit_code != 0
    assert "Error: received 401 HTTP response" in result.output


# Mock the builder and Reddit client behavior
@patch("reddit_topics_aggregator.cli.RedditClientBuilder")
def test_connect_command_with_cli_options(mock_builder, cli: FunctionType):
    """Test the connect command when all CLI options are provided."""
    # Create mock builder and mock Reddit client
    mock_reddit_client = MagicMock()
    mock_reddit_user = MagicMock()
    mock_reddit_user.name = "TestUser"
    mock_reddit_user.id = "user123"
    mock_reddit_user.link_karma = 100
    mock_reddit_user.comment_karma = 200

    # Set the mock builder's return value
    mock_builder_instance = mock_builder.return_value
    mock_builder_instance.build.return_value = mock_reddit_client
    mock_reddit_client.user.me.return_value = mock_reddit_user

    # Invoke the CLI command
    result = cli(
        [
            "connect",
            "--client-id",
            "test_id",
            "--client-secret",
            "test_secret",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )

    # Assert that the command executed successfully
    assert result.exit_code == 0
    assert "Authenticated as: TestUser" in result.output
    assert "User ID: user123" in result.output
    assert "100 link karma" in result.output
    assert "200 comment karma" in result.output

    # Ensure that the builder was called with the correct parameters
    mock_builder_instance.set_client_id.assert_called_once_with("test_id")
    mock_builder_instance.set_client_secret.assert_called_once_with(
        "test_secret"
    )
    mock_builder_instance.set_username.assert_called_once_with("test_user")
    mock_builder_instance.set_password.assert_called_once_with("test_password")
    mock_builder_instance.build.assert_called_once()


@patch("reddit_topics_aggregator.cli.RedditClientBuilder")
@patch.dict(
    "os.environ",
    {
        "REDDIT_CLIENT_ID": "env_id",
        "REDDIT_CLIENT_SECRET": "env_secret",
        "REDDIT_USERNAME": "env_user",
        "REDDIT_PASSWORD": "env_password",
    },
)
def test_connect_command_with_env_vars(mock_builder, cli: FunctionType):
    """Test the connect command using environment variables."""
    # Create mock Reddit client and user
    mock_reddit_client = MagicMock()
    mock_reddit_user = MagicMock()
    mock_reddit_user.name = "EnvUser"
    mock_reddit_user.id = "env_user_id"
    mock_reddit_user.link_karma = 150
    mock_reddit_user.comment_karma = 250

    # Set the mock builder's return value
    mock_builder_instance = mock_builder.return_value
    mock_builder_instance.build.return_value = mock_reddit_client
    mock_reddit_client.user.me.return_value = mock_reddit_user

    # Invoke the CLI command without providing CLI arguments
    result = cli(["connect"])

    # Assert the command ran successfully and output correct user info
    assert result.exit_code == 0
    assert "Authenticated as: EnvUser" in result.output
    assert "User ID: env_user_id" in result.output
    assert "150 link karma" in result.output
    assert "250 comment karma" in result.output

    # Check that the builder used the environment variables
    mock_builder_instance.build.assert_called_once()


@patch("reddit_topics_aggregator.cli.RedditClientBuilder")
def test_connect_command_with_custom_user_agent(
    mock_builder, cli: FunctionType
):
    """Test the connect command with a custom user agent."""
    # Create mock Reddit client and user
    mock_reddit_client = MagicMock()
    mock_reddit_user = MagicMock()
    mock_reddit_user.name = "TestUserAgent"
    mock_reddit_user.id = "user_agent_id"

    # Set the mock builder's return value
    mock_builder_instance = mock_builder.return_value
    mock_builder_instance.build.return_value = mock_reddit_client
    mock_reddit_client.user.me.return_value = mock_reddit_user

    # Invoke the CLI command with a custom user agent
    result = cli(
        [
            "connect",
            "--client-id",
            "test_id",
            "--client-secret",
            "test_secret",
            "--username",
            "test_user",
            "--password",
            "test_password",
            "--user-agent",
            "custom-agent/1.0",
        ]
    )

    # Assert the command ran successfully
    assert result.exit_code == 0
    assert "Authenticated as: TestUserAgent" in result.output

    # Ensure the custom user agent was set
    mock_builder_instance.set_user_agent.assert_called_once_with(
        "custom-agent/1.0"
    )
    mock_builder_instance.build.assert_called_once()


@patch("reddit_topics_aggregator.cli.RedditClientBuilder")
def test_connect_command_praw_exception(mock_builder, cli: FunctionType):
    """Test the connect command when PRAWException is raised by the Reddit client."""
    # Create mock Reddit client and set it to raise PRAWException
    mock_reddit_client = MagicMock()
    mock_reddit_client.user.me.side_effect = praw.exceptions.PRAWException(
        "Test PRAW error"
    )

    # Set the mock builder's return value
    mock_builder_instance = mock_builder.return_value
    mock_builder_instance.build.return_value = mock_reddit_client

    # Invoke the CLI command
    result = cli(
        [
            "connect",
            "--client-id",
            "test_id",
            "--client-secret",
            "test_secret",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )

    # Assert the command exited with an error and printed the correct error message
    assert result.exit_code != 0
    assert "Reddit Client Error: Test PRAW error" in result.output


@patch("reddit_topics_aggregator.cli.RedditClientBuilder")
def test_connect_command_value_error(mock_builder, cli: FunctionType):
    """Test the connect command when ValueError is raised by the Reddit client."""
    # Create mock Reddit client and set it to raise ValueError
    mock_reddit_client = MagicMock()
    mock_reddit_client.user.me.side_effect = ValueError("Test ValueError error")

    # Set the mock builder's return value
    mock_builder_instance = mock_builder.return_value
    mock_builder_instance.build.return_value = mock_reddit_client

    # Invoke the CLI command
    result = cli(
        [
            "connect",
            "--client-id",
            "test_id",
            "--client-secret",
            "test_secret",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )

    # Assert the command exited with an error and printed the correct error message
    assert result.exit_code != 0
    assert "Configuration Error: Test ValueError error" in result.output
    assert "Help: Correct the issue above and try again" in result.output
