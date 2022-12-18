# wire-size

[![PyPI](https://img.shields.io/pypi/v/wire-size)](https://pypi.org/project/wire-size/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wire-size)](https://pypi.org/project/wire-size/)
[![PyPI - License](https://img.shields.io/pypi/l/wire-size)](https://pypi.org/project/wire-size/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/wire-size)](https://pypi.org/project/wire-size/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/wire-size)](https://pypi.org/project/wire-size/)

Test bandwidth to cloud provider endpoint.

Currently, supports:
- digitalocean

## Installation

```bash
pip install wire-size
```

## Usage

```bash
wire-size --help
Usage: wire-size [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  digitalocean
```

```bash
wire-size digitalocean
+------+-----------+                                                                                                                                                                                                                                   
| Area |   Speed   |
+------+-----------+
| nyc1 | 3.40 MB/s |
| nyc2 | 3.24 MB/s |
| nyc3 | 4.22 MB/s |
| ams2 | 2.59 MB/s |
| ams3 | 2.04 MB/s |
| sgp1 | 6.42 MB/s |
| lon1 | 2.79 MB/s |
| fra1 | 2.29 MB/s |
| tor1 | 4.01 MB/s |
| sfo1 | 4.00 MB/s |
| sfo2 | 2.51 MB/s |
| sfo3 | 5.91 MB/s |
| blr1 | 5.06 MB/s |
+------+-----------+
```