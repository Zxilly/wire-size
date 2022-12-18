import click
import requests as requests

from .provider import Provider
from click import Command
from tqdm import tqdm
from time import perf_counter

from prettytable import PrettyTable


class DigitalOceanProvider(Provider):
    # areas = ["nyc1", "nyc2", "nyc3", "ams2", "ams3", "sgp1", "lon1", "fra1", "tor1", "sfo1", "sfo2", "sfo3", "blr1"]
    areas = ["nyc1", "nyc2"]
    download_url_template = "http://speedtest-{}.digitalocean.com/10mb.test"

    @staticmethod
    @click.command()
    def digitalocean():
        statictic = dict()

        for area in DigitalOceanProvider.areas:
            url = DigitalOceanProvider.download_url_template.format(area)

            start_time = perf_counter()

            head_response = requests.head(url)

            size = int(head_response.headers.get("Content-Length", 0))
            if size == 0:
                raise Exception("No content length header")
            with tqdm(total=size, unit="B", unit_scale=True, unit_divisor=1024, desc=area) as pbar:
                response = requests.get(url, stream=True)
                for chunk in response.iter_content(chunk_size=1000):
                    pbar.update(len(chunk))

            end_time = perf_counter()

            download_speed = size / (end_time - start_time)
            statictic[area] = download_speed / 1024 / 1024

        table = PrettyTable()
        table.field_names = ["Area", "Speed"]
        for area, speed in statictic.items():
            table.add_row([area, f"{speed:.2f} MB/s"])
        click.echo(table.get_string())

    @staticmethod
    def command() -> Command:
        return DigitalOceanProvider.digitalocean
