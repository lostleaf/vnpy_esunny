# The MIT License (MIT)
#
# Copyright (c) 2015-present, Xiaoyou Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import ctypes
import os
import sys
from importlib import metadata
from pathlib import Path


def _preload_linux_runtime() -> None:
    """Preload the SDK runtime library that is opened via dlopen()."""
    if not sys.platform.startswith("linux"):
        return

    api_dir: Path = Path(__file__).resolve().parent / "api"
    preload_path: Path = api_dir / "libTapDataCollectAPI.so"

    if not preload_path.is_file():
        raise FileNotFoundError(f"Missing runtime library: {preload_path}")

    mode: int = getattr(os, "RTLD_NOW", 0) | getattr(os, "RTLD_GLOBAL", 0)
    try:
        ctypes.CDLL(str(preload_path), mode=mode)
    except OSError as exc:
        raise OSError(f"Failed to preload {preload_path.name}: {exc}") from exc


_preload_linux_runtime()


def _load_gateway() -> type:
    from .gateway import EsunnyGateway as gateway_cls

    return gateway_cls


EsunnyGateway = _load_gateway()


__all__ = ["EsunnyGateway"]


try:
    __version__ = metadata.version("vnpy_esunny")
except metadata.PackageNotFoundError:
    __version__ = "dev"
