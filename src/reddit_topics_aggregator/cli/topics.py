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
    help='The name of the Subreddits to query. Can be specified without the "r/". e.g. programming or programminghumor',
)
@click.option(
    "--top",
    required=False,
    default=10,
    show_default=True,
    type=int,
    help="Number of top submissions to retrieve from the subreddits",
)
@click.option(
    "--new",
    required=False,
    default=10,
    show_default=True,
    type=int,
    help="Number of newest submissions to retrieve from the subreddits",
)
@click.option(
    "--hot",
    required=False,
    default=10,
    show_default=True,
    type=int,
    help="Number of hottest submissions to retrieve from the subreddits",
)
def topics(
    client_id,
    client_secret,
    username,
    password,
    user_agent,
    subreddit,
    top,
    new,
    hot,
):
    """Extract topics from Subreddits."""
    try:
        handle_missing_api_auth(client_id, client_secret, username, password)
        if all([hot < 1, new < 1, top < 1]):
            raise click.UsageError(
                "Must provide a positive value for one or more of: '--hot', '--new', '--top'"
            )
        reddit_client = RedditClientBuilder.build_reddit_client_from_args(
            client_id, client_secret, username, password, user_agent
        )
        for sub in subreddit:
            ## TODO Start refactor
            topics = []
            this_subreddit = reddit_client.subreddit(sub)
            if top > 0:
                topics.extend(this_subreddit.top(limit=top))
            if new > 0:
                topics.extend(this_subreddit.new(limit=new))
            if hot > 0:
                topics.extend(this_subreddit.hot(limit=hot))
            ## TODO End refactor

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
