import click

from reddit_topics_aggregator.cli.connect import connect
from reddit_topics_aggregator.cli.topics import topics


@click.group()
@click.version_option(
    message="%(version)s", package_name="reddit-topics-aggregator"
)
def reddit_topics_aggregator():
    """Reddit Topics Aggregator is a tool used to aggregate hot, new, top, and rising topics from multiple subreddits."""


reddit_topics_aggregator.add_command(connect)
reddit_topics_aggregator.add_command(topics)
