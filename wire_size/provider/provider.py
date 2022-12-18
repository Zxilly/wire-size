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
        def fn(single):
            if single:
                downloader = SingleDownloader
            else:
                downloader = MultiDownloader

            statistic = dict()

            for area, url in self.urls().items():
                spend_time, file_size = asyncio.run(downloader(area, url).download())
                download_speed = file_size / spend_time
                if spend_time > 0:
                    statistic[area] = statistic[area] = download_speed / 1024 / 1024
                else:
                    statistic[area] = -1

            table = PrettyTable()
            table.field_names = ["Area", "Speed"]
            for area, speed in statistic.items():
                speed_fmt = f"{speed:.2f} MB/s" if speed > 0 else "Less than 100 KB/s"
                table.add_row([area, speed_fmt])
            click.echo(table.get_string())

        return fn
