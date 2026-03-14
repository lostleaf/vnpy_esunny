# VeighNa 框架的易盛底层接口

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-9.0.3.16.1-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-linux%20x86__64-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## 说明

基于易盛启明星 V9 API `9.0.3.16` 的接口封装开发，支持启明星后台系统，适用于内盘交易所交易。

当前仓库只支持 Linux x86_64，不再提供 Windows 编译或安装支持。

## 安装

安装环境推荐基于 4.3.0 版本以上的 [**VeighNa Studio**](https://www.vnpy.com)。

源码安装和开发态安装都使用 `setuptools + setup.py` 构建，构建时会编译两个 pybind11 扩展，并随包分发以下 Linux 运行库：

- `libTapQuoteAPI.so`
- `libTapTradeAPI.so`
- `libTapDataCollectAPI.so`

直接安装：

```bash
pip install vnpy_esunny
```

本地源码安装：

```bash
pip install .
```

开发态安装：

```bash
pip install -e .
```

源码安装前请确认本机具备可用的 Linux C++ 编译环境，例如 `g++`，以及 `pip` 可安装 `setuptools`、`wheel`、`pybind11`。

如需在仓库内直接构建本地验证环境，推荐使用 `uv`：

```bash
uv sync
uv run python -m build --wheel --no-isolation
```

仓库已通过 `.python-version` 将 `uv` 环境固定到 Python `3.13`。

## 使用

以脚本方式启动（`script/run.py`）：

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_esunny import EsunnyGateway


def main():
    """主入口函数"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    main_engine.add_gateway(EsunnyGateway)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
```

## gateway 调整说明

对比之前基于易盛启明星/北斗星兼容交易 API `1.0.2.2` 的封装版本，目前的 `esunny_gateway.py` 做了以下调整：

1. `QuoteApi` 中品种查询、合约查询以及行情订阅函数调用时都需要传入 `session`（`int`）入参。
2. `TradeApi` 采用 `vnpy_tap` 中 `tap_gateway.py` 的方式，登录之后先查询资金、持仓、委托、成交推送一次，后续收到更新再继续推送。
3. `TradeApi` 调用 `insertOrder` 函数进行委托时，新增指定 `TacticsType` 策略单类型、`TriggerCondition` 触发条件类型、`TriggerPriceType` 触发价格类型字段传 `N`，`OrderSource` 委托来源字段传 `A`（`TAPI_ORDER_SOURCE_ESUNNY_API`）。
4. `TradeApi` 调用 `insertOrder` 函数进行委托时，金交所合约的 `HedgeFlag` 投机保值和 `HedgeFlag2` 投机保值 2 都和期货委托一致，传 `TAPI_HEDGEFLAG_T` 投机。
