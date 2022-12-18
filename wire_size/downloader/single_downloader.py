from time import perf_counter

import requests

from wire_size.downloader.downloader import Downloader


class SingleDownloader(Downloader):
    def __init__(self, name, url):
        super().__init__()
        self.name = name
        self.url = url

    async def download(self):
        start_time = perf_counter()

        head_response = requests.head(self.url)

        size = int(head_response.headers["Content-Length"])
        self.render(self.name, size)

        estimate_time = size / 1024 / 100

        response = requests.get(self.url, stream=True)

        for chunk in response.iter_content():
            self.update(len(chunk))

            if perf_counter() - start_time > estimate_time:
                return -1, size

        self.close_bar()

        return perf_counter() - start_time, size
