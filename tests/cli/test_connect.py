from types import FunctionType
from unittest.mock import MagicMock, patch

import praw.exceptions


def test_cli_connect(cli: FunctionType):
    result = cli(["connect"])
    assert result.exit_code != 0
    assert (
        "Try 'reddit-topics-aggregator connect --help' for help."
    ) in result.output
    assert (
        "Error: Missing option '--client-id'"
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
@patch("reddit_topics_aggregator.cli.connect.RedditClientBuilder")
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
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client
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
    mock_builder.build_reddit_client_from_args.assert_called_once_with(
        "test_id", "test_secret", "test_user", "test_password", None
    )


@patch("reddit_topics_aggregator.cli.connect.RedditClientBuilder")
@patch.dict(
    "os.environ",
    {
        "REDDIT_CLIENT_ID": "env_id",
        "REDDIT_CLIENT_SECRET": "env_secret",
        "REDDIT_USERNAME": "env_user",
        "REDDIT_PASSWORD": "env_password",
        "REDDIT_USER_AGENT": "env_user_agent",
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
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client
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
    mock_builder.build_reddit_client_from_args.assert_called_once_with(
        "env_id", "env_secret", "env_user", "env_password", "env_user_agent"
    )


@patch("reddit_topics_aggregator.cli.connect.RedditClientBuilder")
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
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client
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
    mock_builder.build_reddit_client_from_args.assert_called_once_with(
        "test_id",
        "test_secret",
        "test_user",
        "test_password",
        "custom-agent/1.0",
    )


@patch("reddit_topics_aggregator.cli.connect.RedditClientBuilder")
def test_connect_command_praw_exception(mock_builder, cli: FunctionType):
    """Test the connect command when PRAWException is raised by the Reddit client."""
    # Create mock Reddit client and set it to raise PRAWException
    mock_reddit_client = MagicMock()
    mock_reddit_client.user.me.side_effect = praw.exceptions.PRAWException(
        "Test PRAW error"
    )

    # Set the mock builder's return value
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client

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


@patch("reddit_topics_aggregator.cli.connect.RedditClientBuilder")
def test_connect_command_value_error(mock_builder, cli: FunctionType):
    """Test the connect command when ValueError is raised by the Reddit client."""
    # Create mock Reddit client and set it to raise ValueError
    mock_reddit_client = MagicMock()
    mock_reddit_client.user.me.side_effect = ValueError("Test ValueError error")

    # Set the mock builder's return value
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client

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
