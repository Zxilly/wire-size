import click
from provider import __all__ as providers


@click.group()
def group():
    click.echo("Start testing...")


for p in providers:
    group.add_command(p.command())

if __name__ == '__main__':
    group()
