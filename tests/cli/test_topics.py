from collections.abc import Generator
from types import FunctionType
from unittest.mock import MagicMock, patch

import praw.exceptions
import pytest
from praw.models import Submission

TEST_SUBREDDIT_NAME = "mysubreddit"

@pytest.fixture(scope="function")
def topic_cli_options() -> Generator[list[str]]:
    yield [
    "topics",
    "--client-id",
    "test_id",
    "--client-secret",
    "test_secret",
    "--username",
    "test_user",
    "--password",
    "test_password",
    "--subreddit",
    TEST_SUBREDDIT_NAME,
]

TEST_TOPIC_SUBMISSON = Submission(
    reddit="praw.Reddit",
    _data={
        "id": "1fxukkw",
        "title": "topic title",
        "selftext": "topic content",
        "url": "https://www.reddit.com/r/mysubreddit/comments/1fxukkw/topic_title/",
        "score": 20,
    },
)


def test_topics(cli: FunctionType):
    result = cli(["topics"])
    assert result.exit_code != 0
    assert (
        "Try 'reddit-topics-aggregator topics --help' for help."
    ) in result.output
    assert ("Error: Missing option '--subreddit'") in result.output


def test_topics_with_subreddit(cli: FunctionType):
    result = cli(["topics", "--subreddit", TEST_SUBREDDIT_NAME])
    assert result.exit_code != 0
    assert (
        "Try 'reddit-topics-aggregator topics --help' for help."
    ) in result.output
    assert (
        "Error: Missing required options: --client-id, --client-secret, --username, --password"
    ) in result.output


def test_topics_401_authentication_error(cli: FunctionType, topic_cli_options: list[str]):
    result = cli(topic_cli_options)
    assert result.exit_code != 0
    assert "Error: received 401 HTTP response" in result.output


# Mock the builder and Reddit client behavior
@patch("reddit_topics_aggregator.cli.topics.RedditClientBuilder")
def test_topics_with_cli_options(mock_builder, cli: FunctionType, topic_cli_options: list[str]):
    """Test the topics command when all CLI options are provided."""
    # Create mock builder and mock Reddit client
    mock_reddit_client = MagicMock()
    mock_subreddit = MagicMock()
    mock_subreddit.display_name = TEST_SUBREDDIT_NAME
    mock_subreddit.title = "My Subreddit"
    mock_subreddit.top.return_value = [TEST_TOPIC_SUBMISSON]

    # Set the mock builder's return value
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client
    mock_reddit_client.subreddit.return_value = mock_subreddit

    # Invoke the CLI command
    result = cli(topic_cli_options)

    # Assert that the command executed successfully
    assert result.exit_code == 0
    assert "Subreddit: r/mysubreddit (My Subreddit)" in result.output
    assert "Topic: topic title" in result.output
    assert (
        "Topic URL: https://www.reddit.com/r/mysubreddit/comments/1fxukkw/topic_title/"
        in result.output
    )
    assert "Content: topic content" in result.output

    # Ensure that the builder was called with the correct parameters
    mock_builder.build_reddit_client_from_args.assert_called_once_with(
        "test_id", "test_secret", "test_user", "test_password", None
    )


# Mock the builder and Reddit client behavior
@patch("reddit_topics_aggregator.cli.topics.RedditClientBuilder")
def test_topics_with_top_option(mock_builder, cli: FunctionType, topic_cli_options: list[str]):
    """Test the topics command when all CLI options are provided and top option."""
    # Create mock builder and mock Reddit client
    count_topics = 5
    mock_reddit_client = MagicMock()
    mock_subreddit = MagicMock()
    mock_subreddit.display_name = TEST_SUBREDDIT_NAME
    mock_subreddit.title = "My Subreddit"
    mock_subreddit.top.return_value = [TEST_TOPIC_SUBMISSON] * count_topics

    # Set the mock builder's return value
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client
    mock_reddit_client.subreddit.return_value = mock_subreddit

    # Invoke the CLI command

    cli_options = topic_cli_options
    cli_options.extend(["--top", str(count_topics)])
    print(cli_options)
    result = cli(cli_options)

    # Assert that the command executed successfully
    assert result.exit_code == 0
    assert (
        result.output.count("Subreddit: r/mysubreddit (My Subreddit)")
        == count_topics
    )
    assert result.output.count("Topic: topic title") == count_topics
    assert (
        result.output.count(
            "Topic URL: https://www.reddit.com/r/mysubreddit/comments/1fxukkw/topic_title/"
        )
        == count_topics
    )
    assert result.output.count("Content: topic content") == count_topics


@patch("reddit_topics_aggregator.cli.topics.RedditClientBuilder")
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
def test_topics_with_env_vars(mock_builder, cli: FunctionType):
    """Test the topics command using environment variables."""
    # Create mock Reddit client and user
    mock_reddit_client = MagicMock()
    mock_subreddit = MagicMock()
    mock_subreddit.display_name = TEST_SUBREDDIT_NAME
    mock_subreddit.title = "My Subreddit"
    mock_subreddit.top.return_value = [TEST_TOPIC_SUBMISSON]

    # Set the mock builder's return value
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client
    mock_reddit_client.subreddit.return_value = mock_subreddit

    # Invoke the CLI command without providing CLI arguments
    result = cli(["topics", "-s", TEST_SUBREDDIT_NAME])

    # Assert the command ran successfully and output correct user info
    assert result.exit_code == 0
    assert "Subreddit: r/mysubreddit (My Subreddit)" in result.output
    assert "Topic: topic title" in result.output
    assert (
        "Topic URL: https://www.reddit.com/r/mysubreddit/comments/1fxukkw/topic_title/"
        in result.output
    )
    assert "Content: topic content" in result.output

    # Ensure that the builder was called with the correct parameters
    mock_builder.build_reddit_client_from_args.assert_called_once_with(
        "env_id", "env_secret", "env_user", "env_password", "env_user_agent"
    )


@patch("reddit_topics_aggregator.cli.topics.RedditClientBuilder")
def test_topics_handles_praw_exception(mock_builder, cli: FunctionType, topic_cli_options: list[str]):
    """Test the topics command when PRAWException is raised by the Reddit client."""
    # Create mock Reddit client and set it to raise PRAWException
    mock_reddit_client = MagicMock()
    mock_reddit_client.subreddit.side_effect = praw.exceptions.PRAWException(
        "Test PRAW error"
    )

    # Set the mock builder's return value
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client

    # Invoke the CLI command
    result = cli(topic_cli_options)

    # Assert the command exited with an error and printed the correct error message
    assert result.exit_code != 0
    assert "Reddit Client Error: Test PRAW error" in result.output


@patch("reddit_topics_aggregator.cli.topics.RedditClientBuilder")
def test_topics_handles_value_error(mock_builder, cli: FunctionType, topic_cli_options: list[str]):
    """Test the topics command when ValueError is raised by the Reddit client."""
    # Create mock Reddit client and set it to raise ValueError
    mock_reddit_client = MagicMock()
    mock_reddit_client.subreddit.side_effect = ValueError(
        "Test ValueError error"
    )

    # Set the mock builder's return value
    mock_builder.build_reddit_client_from_args.return_value = mock_reddit_client

    # Invoke the CLI command
    result = cli(topic_cli_options)

    # Assert the command exited with an error and printed the correct error message
    assert result.exit_code != 0
    assert "Configuration Error: Test ValueError error" in result.output
    assert "Help: Correct the issue above and try again" in result.output


def test_topics_with_0_additional_options(cli: FunctionType, topic_cli_options: list[str]):
    """Test the topics command when all CLI options are provided and --top=0, --new=0."""
    # Invoke the CLI command
    cli_options = topic_cli_options
    cli_options.extend(["--top", "0", "--new", "0"])

    result = cli(cli_options)

    # Assert that the command executed successfully
    assert result.exit_code != 0
    assert (
        "Try 'reddit-topics-aggregator topics --help' for help."
    ) in result.output
    assert (
        "Error: Must provide a positive value for one or more of: '--new', '--top'"
        in result.output
    )


@patch("reddit_topics_aggregator.cli.topics.RedditClientBuilder")
def test_topics_with_0_top_option(mock_builder, cli: FunctionType, topic_cli_options: list[str]):
    """Test the topics command when all CLI options are provided and --top=0."""
    # Invoke the CLI command
    cli_options = topic_cli_options
    cli_options.extend(["--top", "0"])

    result = cli(cli_options)

    # Assert that the command executed successfully
    assert result.exit_code == 0


@patch("reddit_topics_aggregator.cli.topics.RedditClientBuilder")
def test_topics_with_0_new_option(mock_builder, cli: FunctionType, topic_cli_options: list[str]):
    """Test the topics command when all CLI options are provided and --new=0."""
    # Invoke the CLI command
    cli_options = topic_cli_options
    cli_options.extend(["--new", "0"])

    result = cli(cli_options)

    # Assert that the command executed successfully
    assert result.exit_code == 0
