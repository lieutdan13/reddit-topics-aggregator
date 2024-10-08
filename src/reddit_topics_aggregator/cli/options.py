import click

option_client_id = click.option(
    "--client-id",
    default=None,
    envvar="REDDIT_CLIENT_ID",
    help="Reddit API client ID",
)
option_client_secret = click.option(
    "--client-secret",
    default=None,
    envvar="REDDIT_CLIENT_SECRET",
    help="Reddit API client secret",
)
option_username = click.option(
    "--username", default=None, envvar="REDDIT_USERNAME", help="Reddit username"
)
option_password = click.option(
    "--password", default=None, envvar="REDDIT_PASSWORD", help="Reddit password"
)
option_user_agent = click.option(
    "--user-agent",
    default=None,
    envvar="REDDIT_USER_AGENT",
    help="Custom user agent",
)


def reddit_api_auth(function: callable):
    for option in reversed(
        [
            option_client_id,
            option_client_secret,
            option_username,
            option_password,
            option_user_agent,
        ]
    ):
        function = option(function)
    return function
