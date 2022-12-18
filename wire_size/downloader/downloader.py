import time

from .utils import *


class Downloader:
    def __init__(self, url, num_tasks=16):
        self.bar = None
        self.blocks = None
        self.size = None
        self.url = url
        self.num_tasks = num_tasks
        self.max_tries = 3
        self.session = aiohttp.ClientSession(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54', },
            loop=asyncio.get_event_loop()
        )

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
                self.bar.update(len(chunk))
        del self.blocks[block_id]

    async def download(self) -> (int, int):
        with connecting():
            self.size, file_type = await self.get_download_info()

        self.blocks = self.split()

        start_time = time.perf_counter()

        if self.num_tasks > self.size:
            tqdm.write(
                'Too many tasks (%d > file size %d), using 1 task' %
                (self.num_tasks, self.size)
            )
            self.num_tasks = 1
        downloaded_size = 0

        formatted_size = tqdm.format_sizeof(self.size, 'B', 1024)
        if downloaded_size:
            formatted_size += ' (already downloaded {})'.format(
                tqdm.format_sizeof(downloaded_size, 'B', 1024))
        print_colored_kv('Size', formatted_size)
        print_colored_kv('Type', file_type)
        tqdm.write('')

        self.bar = tqdm(
            initial=downloaded_size,
            dynamic_ncols=True,
            total=self.size,
            unit='B', unit_scale=True, unit_divisor=1024
        )

        await asyncio.gather(
            *(self.download_block(id) for id in self.blocks)
        )
        end_time = time.perf_counter()

        return end_time - start_time, self.size

    async def close(self):
        await self.session.close()
        self.bar.close()
