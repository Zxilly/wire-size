import asyncio
import time

import aiohttp
from tqdm import tqdm

from .utils import retry, ClosedRange
from .downloader import Downloader


class MultiDownloader(Downloader):
    def __init__(self, name, url, num_tasks=4):
        super().__init__()
        self.bar = None
        self.blocks = None
        self.size = None
        self.name = name
        self.url = url
        self.num_tasks = num_tasks
        self.max_tries = 3
        self.session = None

    @retry
    async def get_download_info(self):
        async with self.session.head(
                self.url, allow_redirects=True
        ) as response:
            response.raise_for_status()
            # Use redirected URL
            self.url = str(response.url)
            return (
                int(response.headers['Content-Length']),
                response.headers['Content-Type']
            )

    def split(self):
        part_len, remain = divmod(self.size, self.num_tasks)
        blocks = {
            i: ClosedRange(
                begin=i * part_len,
                end=(i + 1) * part_len - 1
            ) for i in range(self.num_tasks - 1)
        }
        blocks[self.num_tasks - 1] = ClosedRange(
            begin=(self.num_tasks - 1) * part_len,
            end=self.size - 1
        )
        return blocks

    @retry
    async def download_block(self, block_id):
        header = {'Range': 'bytes={}-{}'.format(*self.blocks[block_id])}
        async with self.session.get(self.url, headers=header) as response:
            response.raise_for_status()
            async for chunk in response.content.iter_any():
                self.blocks[block_id].begin += len(chunk)
                self.update(len(chunk))
        del self.blocks[block_id]

    async def require_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54', },
                loop=asyncio.get_event_loop()
            )

    async def download(self) -> (float, int):
        await self.require_session()

        self.size, file_type = await self.get_download_info()

        self.blocks = self.split()

        start_time = time.perf_counter()

        if self.num_tasks > self.size:
            self.num_tasks = 1

        self.render(self.name, self.size)
        await asyncio.gather(
            *(self.download_block(block_id) for block_id in self.blocks)
        )

        end_time = time.perf_counter()

        await self.close()

        return end_time - start_time, self.size

    async def close(self):
        await self.session.close()
        self.close_bar()
