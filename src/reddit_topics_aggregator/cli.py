import click
import praw
import praw.exceptions

from reddit_topics_aggregator.reddit_client_builder import RedditClientBuilder


@click.group()
@click.version_option(
    message="%(version)s", package_name="reddit-topics-aggregator"
)
def main():
    """Default cli command without a sub-command."""


@main.command()
@click.option("--client-id", default=None, help="Reddit client ID")
@click.option("--client-secret", default=None, help="Reddit client secret")
@click.option("--username", default=None, help="Reddit username")
@click.option("--password", default=None, help="Reddit password")
@click.option("--user-agent", default=None, help="Custom user agent")
def connect(client_id, client_secret, username, password, user_agent):
    """Connect to Reddit and display the authenticated user's information."""
    try:
        builder = RedditClientBuilder()

        if client_id:
            builder.set_client_id(client_id)
        if client_secret:
            builder.set_client_secret(client_secret)
        if username:
            builder.set_username(username)
        if password:
            builder.set_password(password)
        if user_agent:
            builder.set_user_agent(user_agent)

        # Build the Reddit client
        reddit_client = builder.build()

        # Fetch and display the authenticated user's information
        authenticated_user = reddit_client.user.me()
        click.echo(f"Authenticated as: {authenticated_user.name}")
        click.echo(f"User ID: {authenticated_user.id}")
        click.echo(
            f"Karma: {authenticated_user.link_karma} link karma, {authenticated_user.comment_karma} comment karma"
        )

    except praw.exceptions.PRAWException as e:
        click.echo(f"Reddit Client Error: {e}", err=True)
        raise click.ClickException(str(e)) from e
    except ValueError as e:
        if str(e).startswith("Missing required fields: "):
            err_msg = "Missing arguments: "
            missing_fields = extract_fields_from_exception(e)
            missing_fields_str = "--" + (", --".join(missing_fields))

            click.echo(
                f"Configuration Error: {err_msg}{missing_fields_str}", err=True
            )
            raise click.ClickException(
                "Help: Specify the arguments above and try again"
            ) from e
        else:
            click.echo(f"Configuration Error: {e}", err=True)
            raise click.ClickException(
                "Help: Correct the issue above and try again"
            ) from e
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.ClickException(str(e)) from e


def extract_fields_from_exception(e):
    return (
        str(e)
        .replace("Missing required fields: ", "")
        .replace("_", "-")
        .split(", ")
    )
