from typing import Dict

from wire_size.provider.provider import Provider


class DigitalOceanProvider(Provider):
    name: str = "digitalocean"

    areas = ["nyc1", "nyc2", "nyc3", "ams2", "ams3", "sgp1", "lon1", "fra1", "tor1", "sfo1", "sfo2", "sfo3", "blr1"]
    download_url_template = "http://speedtest-{}.digitalocean.com/10mb.test"

    def urls(self) -> Dict[str, str]:
        ret = dict()
        for area in self.areas:
            ret[area] = self.download_url_template.format(area)
        return ret
