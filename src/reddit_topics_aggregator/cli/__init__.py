import click

from .connect import connect as connect_command
from .topics import topics as topics_command


@click.group()
@click.version_option(
    message="%(version)s", package_name="reddit-topics-aggregator"
)
def reddit_topics_aggregator():
    """Reddit Topics Aggregator is a tool used to aggregate hot, new, top, and rising topics from multiple Subreddits."""


reddit_topics_aggregator.add_command(connect_command)
reddit_topics_aggregator.add_command(topics_command)
