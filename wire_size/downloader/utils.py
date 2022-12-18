import asyncio
import functools
import socket
from contextlib import contextmanager
from random import choice

import aiohttp
from termcolor import colored, COLORS
from tqdm import tqdm

colors = list(COLORS)


def print_colored_kv(k, v):
    tqdm.write(
        colored('  ' + k + ': ', color=choice(colors), attrs=['bold']) +
        colored(v, color='white', attrs=['bold'])
    )


class ClosedRange:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __iter__(self):
        yield self.begin
        yield self.end

    def __str__(self):
        return '[{0.begin}, {0.end}]'.format(self)

    @property
    def size(self):
        return self.end - self.begin + 1


def retry(coro_func):
    @functools.wraps(coro_func)
    async def wrapper(self, *args, **kwargs):
        tried = 0
        while True:
            tried += 1
            try:
                return await coro_func(self, *args, **kwargs)
            except (aiohttp.ClientError, socket.gaierror) as exc:
                try:
                    if 400 <= exc.code < 500:
                        raise exc
                except AttributeError:
                    pass
                if tried <= self.max_tries:
                    sec = tried / 2
                    await asyncio.sleep(sec)
                else:
                    raise exc
            except asyncio.TimeoutError:
                await asyncio.sleep(1)

    return wrapper


@contextmanager
def connecting(msg='Connecting'):
    length = len(msg)
    tqdm.write(colored(msg, 'grey', attrs=['bold']),end='')

    async def print_dots():
        while True:
            try:
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            tqdm.write(colored('.', 'grey', attrs=['bold']), end='')
            nonlocal length
            length += 1

    fut = asyncio.ensure_future(print_dots())
    try:
        yield
    finally:
        fut.cancel()
        print('\r' + ' ' * length)
