import click

from reddit_topics_aggregator.reddit_client_builder import RedditClientBuilder

from .exception_handling import handle_cli_exception
from .options import handle_missing_api_auth, reddit_api_auth


@click.command()
@reddit_api_auth
def connect(client_id, client_secret, username, password, user_agent):
    """Connect to Reddit and display username, user id, and Karma about the authenticated user."""
    try:
        handle_missing_api_auth(client_id, client_secret, username, password)
        reddit_client = RedditClientBuilder.build_reddit_client_from_args(
            client_id, client_secret, username, password, user_agent
        )

        # Fetch and display the authenticated user's information
        authenticated_user = reddit_client.user.me()
        click.echo(f"Authenticated as: {authenticated_user.name}")
        click.echo(f"User ID: {authenticated_user.id}")
        click.echo(
            f"Karma: {authenticated_user.link_karma} link karma, {authenticated_user.comment_karma} comment karma"
        )
    except Exception as e:
        handle_cli_exception(e)
