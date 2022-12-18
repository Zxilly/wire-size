import click
from wire_size.provider import __all__ as providers


@click.group()
def group():
    pass


for p in providers:
    group.add_command(p().command())

if __name__ == '__main__':
    group()
