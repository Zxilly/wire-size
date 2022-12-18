from typing import List

from wire_size.provider.digitalocean import DigitalOceanProvider
from wire_size.provider.provider import Provider

__all__: List[Provider] = [DigitalOceanProvider]
