import click



@click.group()
@click.version_option(
    message="%(version)s", package_name="reddit-topics-aggregator"
)
def main():
    """Default cli command without a sub-command."""
