import asyncio
from abc import ABC, abstractmethod

import click as click
from click import Command
from prettytable import PrettyTable
from typing import Dict

from wire_size.downloader import MultiDownloader
from wire_size.downloader.single_downloader import SingleDownloader


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
        @click.option('--single', is_flag=True, help='Test with single connection', default=False)
        @click.option('--multi', is_flag=True, help='Test with multiple connections', default=True)
        def fn(single, multi):
            if single and multi:
                click.echo('You can only choose one mode')
                return
            if not single and not multi:
                click.echo('You must choose one mode')
                return

            if single:
                downloader = SingleDownloader
            else:
                downloader = MultiDownloader

            statistic = dict()

            for area, url in self.urls().items():
                spend_time, file_size = asyncio.run(downloader(area, url).download())
                download_speed = file_size / spend_time
                statistic[area] = download_speed / 1024 / 1024

            table = PrettyTable()
            table.field_names = ["Area", "Speed"]
            for area, speed in statistic.items():
                table.add_row([area, f"{speed:.2f} MB/s"])
            click.echo(table.get_string())

        return fn
