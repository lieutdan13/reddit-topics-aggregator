import click


@click.group(invoke_without_command=True)
@click.version_option(
    message="%(version)s", package_name="reddit-topics-aggregator"
)
@click.argument("input_str", required=False)
@click.option(
    "--capitalize", is_flag=True, required=False, help="Capitalize string"
)
def main(input_str: str | None = None, capitalize: bool = False):
    """Entry point for the application script.

    Args:
        input_str: string to reverse
        capitalize: if true, capitalize letters of input_str
    """
    if input_str is None:
        click.echo("Hello, Reddit Topics Aggregator!")
        return

    from .simple import reverse

    result = reverse(input_str)
    if capitalize:
        result = result.upper()

    click.echo(
        f"{input_str} --reverse{'+capitalize' if capitalize else ''}-> {result}"
    )
