from abc import abstractmethod

from tqdm import tqdm


class Downloader:
    def __init__(self):
        self.bar = None

    def render(self, name, total):
        self.bar = tqdm(
            initial=0,
            dynamic_ncols=True,
            total=total,
            unit='B', unit_scale=True, unit_divisor=1024,
            leave=False, position=0,
            desc=name
        )

    def update(self, size):
        self.bar.update(size)

    def close_bar(self):
        self.bar.close()

    @abstractmethod
    def download(self) -> (int, int):
        pass
