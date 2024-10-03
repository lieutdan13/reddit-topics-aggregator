import pytest
from unittest.mock import patch

from praw import Reddit

from reddit_topics_aggregator.reddit_client_builder import RedditClientBuilder

package_version = "0.0.1"

def test_successful_build():
    """Test building Reddit client when all arguments are passed."""
    builder = RedditClientBuilder()

    # Set all required fields using method arguments
    reddit_client = (
        builder.set_client_id('test_id')
               .set_client_secret('test_secret')
               .set_username('test_user')
               .set_password('test_password')
               .build()
    )

    assert isinstance(reddit_client, Reddit)
    assert reddit_client.config.client_id == 'test_id'
    assert reddit_client.config.client_secret == 'test_secret'
    assert reddit_client.config.username == 'test_user'
    assert reddit_client.config.password == 'test_password'
    assert reddit_client.config.user_agent == f"reddit-topics-aggregator / {package_version}"


@patch.dict('os.environ', {
    'REDDIT_CLIENT_ID': 'env_id',
    'REDDIT_CLIENT_SECRET': 'env_secret',
    'REDDIT_USERNAME': 'env_user',
    'REDDIT_PASSWORD': 'env_password',
    'REDDIT_USER_AGENT': 'env_user_agent'
})
def test_build_with_env_vars():
    """Test building Reddit client using environment variables."""
    builder = RedditClientBuilder()

    # Build client without explicitly setting fields
    reddit_client = builder.build()

    assert isinstance(reddit_client, Reddit)
    assert reddit_client.config.client_id == 'env_id'
    assert reddit_client.config.client_secret == 'env_secret'
    assert reddit_client.config.username == 'env_user'
    assert reddit_client.config.password == 'env_password'
    assert reddit_client.config.user_agent == 'env_user_agent'


def test_missing_required_fields():
    """Test that ValueError is raised if required fields are missing."""
    builder = RedditClientBuilder()

    # Test missing client_id
    with pytest.raises(ValueError, match="client_id"):
        builder.build()

    # Test missing client_secret
    builder.set_client_id('test_id')
    with pytest.raises(ValueError, match="client_secret"):
        builder.build()

    # Test missing username
    builder.set_client_secret('test_secret')
    with pytest.raises(ValueError, match="username"):
        builder.build()

    # Test missing password
    builder.set_username('test_user')
    with pytest.raises(ValueError, match="password"):
        builder.build()
