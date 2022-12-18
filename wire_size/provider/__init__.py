from typing import List

from .digitalocean import DigitalOceanProvider
from .provider import Provider

__all__: List[Provider] = [DigitalOceanProvider]
