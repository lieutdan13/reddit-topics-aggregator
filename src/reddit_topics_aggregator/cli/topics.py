import click

from reddit_topics_aggregator.reddit_client_builder import RedditClientBuilder

from .exception_handling import handle_cli_exception
from .options import handle_missing_api_auth, reddit_api_auth


@click.command()
@reddit_api_auth
@click.option(
    "--subreddit",
    "-s",
    required=True,
    default=None,
    multiple=True,
    help='The name of the Subreddits to query. Can be specified with or without the "r/". e.g. r/programming or programming',
)
def topics(
    client_id,
    client_secret,
    username,
    password,
    user_agent,
    subreddit,
):
    """Extract topics from Subreddits."""
    try:
        handle_missing_api_auth(client_id, client_secret, username, password)
        reddit_client = RedditClientBuilder.build_reddit_client_from_args(
            client_id, client_secret, username, password, user_agent
        )
        click.echo(subreddit)
        for sub in subreddit:
            topics = []
            this_subreddit = reddit_client.subreddit(sub)
            topics.extend(this_subreddit.top(limit=10))

            for topic in topics:
                click.echo("=" * 50)
                click.echo(
                    f"Subreddit: r/{this_subreddit.display_name} ({this_subreddit.title})"
                )
                click.echo(f"Topic: {topic.title}")
                click.echo(f"Topic URL: {topic.url}")
                click.echo(f"Content: {topic.selftext}\n")

    except Exception as e:
        handle_cli_exception(e)
