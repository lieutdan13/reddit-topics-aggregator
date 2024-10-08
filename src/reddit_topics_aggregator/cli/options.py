import click

option_client_id = click.option(
    "--client-id",
    default=None,
    required=False,  # Enforced using custom code
    envvar="REDDIT_CLIENT_ID",
    help="Reddit API client ID",
)
option_client_secret = click.option(
    "--client-secret",
    default=None,
    required=False,  # Enforced using custom code
    envvar="REDDIT_CLIENT_SECRET",
    help="Reddit API client secret",
)
option_username = click.option(
    "--username",
    default=None,
    required=False,  # Enforced using custom code
    envvar="REDDIT_USERNAME",
    help="Reddit username",
)
option_password = click.option(
    "--password",
    default=None,
    required=False,  # Enforced using custom code
    envvar="REDDIT_PASSWORD",
    help="Reddit password",
)
option_user_agent = click.option(
    "--user-agent",
    default=None,
    required=False,
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


def handle_missing_api_auth(client_id, client_secret, username, password):
    # Collect all missing required options
    missing_options = []
    if not client_id:
        missing_options.append("--client-id")
    if not client_secret:
        missing_options.append("--client-secret")
    if not username:
        missing_options.append("--username")
    if not password:
        missing_options.append("--password")

    # If there are missing options, raise an error listing all of them
    if missing_options:
        raise click.UsageError(
            f"Missing required options: {', '.join(missing_options)}"
        )
