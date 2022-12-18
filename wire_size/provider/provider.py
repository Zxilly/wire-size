import asyncio
from abc import ABC, abstractmethod
from typing import Dict

import click as click
from click import Command
from prettytable import PrettyTable

from wire_size.downloader import Downloader


class Provider(ABC):

    @abstractmethod
    def urls(self) -> Dict[str, str]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def command(self) -> Command:

        @click.command(name=self.name)
        def fn():
            statistic = dict()

            for area, url in self.urls().items():
                spend_time, file_size = asyncio.run(Downloader(url).download())
                download_speed = file_size / spend_time
                statistic[area] = download_speed / 1024 / 1024

            table = PrettyTable()
            table.field_names = ["Area", "Speed"]
            for area, speed in statistic.items():
                table.add_row([area, f"{speed:.2f} MB/s"])
            click.echo(table.get_string())

        return fn
