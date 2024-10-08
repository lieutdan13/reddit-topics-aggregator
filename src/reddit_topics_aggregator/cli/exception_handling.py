import click
import praw.exceptions


def handle_cli_exception(e):
    if isinstance(e, praw.exceptions.PRAWException):
        handle_praw_exception(e)
    elif isinstance(e, ValueError):
        handle_value_error(e)
    else:
        handle_general_exception(e)


def handle_general_exception(e):
    click.echo(f"Error: {e}", err=True)
    raise click.ClickException(str(e)) from e


def handle_value_error(e):
    if str(e).startswith("Missing required fields: "):
        handle_missing_fields(e)
    else:
        handle_config_error(e)


def handle_config_error(e):
    click.echo(f"Configuration Error: {e}", err=True)
    raise click.ClickException(
        "Help: Correct the issue above and try again"
    ) from e


def handle_missing_fields(e):
    err_msg = "Missing arguments: "
    missing_fields = extract_fields_from_exception(e)
    missing_fields_str = "--" + (", --".join(missing_fields))

    click.echo(f"Configuration Error: {err_msg}{missing_fields_str}", err=True)
    raise click.ClickException(
        "Help: Specify the arguments above and try again"
    ) from e


def handle_praw_exception(e):
    click.echo(f"Reddit Client Error: {e}", err=True)
    raise click.ClickException(str(e)) from e


def extract_fields_from_exception(e):
    return (
        str(e)
        .replace("Missing required fields: ", "")
        .replace("_", "-")
        .split(", ")
    )
