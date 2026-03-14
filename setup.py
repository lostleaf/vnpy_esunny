from __future__ import annotations

import platform
from pathlib import Path

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup


ROOT: Path = Path(__file__).resolve().parent
API_DIR: Path = ROOT / "vnpy_esunny" / "api"
INCLUDE_DIR: Path = API_DIR / "include"
VNESUNNY_DIR: Path = API_DIR / "vnesunny"

REQUIRED_LIBS: tuple[str, ...] = (
    "libTapQuoteAPI.so",
    "libTapTradeAPI.so",
    "libTapDataCollectAPI.so",
)


def ensure_linux_x86_64() -> None:
    if platform.system() != "Linux":
        raise RuntimeError("vnpy_esunny only supports Linux builds.")

    machine: str = platform.machine().lower()
    if machine not in {"x86_64", "amd64"}:
        raise RuntimeError(f"vnpy_esunny only supports Linux x86_64, got: {platform.machine()}")


def ensure_vendor_libs() -> None:
    missing: list[str] = [name for name in REQUIRED_LIBS if not (API_DIR / name).is_file()]
    if missing:
        missing_text: str = ", ".join(missing)
        raise RuntimeError(f"Missing vendor runtime libraries in {API_DIR}: {missing_text}")


ensure_linux_x86_64()
ensure_vendor_libs()

common_kwargs: dict[str, object] = {
    "include_dirs": [str(INCLUDE_DIR), str(VNESUNNY_DIR)],
    "library_dirs": [str(API_DIR)],
    "runtime_library_dirs": ["$ORIGIN"],
    "cxx_std": 17,
}

ext_modules = [
    Pybind11Extension(
        "vnpy_esunny.api.vnesunnymd",
        ["vnpy_esunny/api/vnesunny/vnesunnymd/vnesunnymd.cpp"],
        libraries=["TapQuoteAPI"],
        **common_kwargs,
    ),
    Pybind11Extension(
        "vnpy_esunny.api.vnesunnytd",
        ["vnpy_esunny/api/vnesunny/vnesunnytd/vnesunnytd.cpp"],
        libraries=["TapTradeAPI"],
        **common_kwargs,
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
