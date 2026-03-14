# 仓库说明

本仓库是 `VeighNa` 框架的易盛启明星 V9 网关实现，发布包名为 `vnpy_esunny`。代码分成两层：

- Python 网关层：负责把 `vnpy` 的对象、枚举和值映射到易盛接口。
- C++/pybind11 扩展层：负责把底层 `TapQuoteAPI`/`TapTradeAPI` 暴露给 Python。

目标不是通用 Web 服务或脚本工具，而是一个需要本地编译和柜台环境配合的交易网关包。

## 目录重点

- `vnpy_esunny/gateway/esunny_gateway.py`
  核心业务文件。大部分 Python 侧行为、字段映射、登录/订阅/委托流程都在这里。

- `vnpy_esunny/api/__init__.py`
  Python 导出面，直接导入 `vnesunnymd` 和 `vnesunnytd` 两个扩展模块。

- `vnpy_esunny/__init__.py`
  包入口。这里有 Windows 下 DLL 搜索路径处理，改动时不要破坏 `TapDataCollectAPI.dll` 的加载逻辑。

- `vnpy_esunny/api/vnesunny/`
  C++ 工程和 pybind11 扩展源码，分别对应行情和交易两个模块。

- `vnpy_esunny/api/include/esunny/`
  易盛头文件。通常作为生成器和 C++ 封装的上游定义来源。

- `vnpy_esunny/api/generator/`
  生成脚本目录。若常量、结构体或接口签名需要批量同步，优先考虑从这里重新生成，而不是手改大段生成结果。

- `script/run.py`
  本地手工联调入口，用于启动 VeighNa GUI 并加载 `EsunnyGateway`。

## 开发约束

- 设置项名称使用中文键（如“行情账号”“交易服务器”），这是网关对外接口的一部分，改名会影响 UI 和已有配置。
- 映射表通常成对出现，例如 `ES2VT` 和 `VT2ES`。修改一侧时，检查另一侧是否也需要同步。
- 该仓库包含 DLL、LIB、头文件和 C++ 工程文件。除非任务明确要求，不要升级或替换这些二进制依赖。
- `esunny_constant.py` 体量大且明显偏生成产物。若要做系统性常量更新，优先查生成脚本和头文件来源。
- 这是交易接口代码，优先避免“看起来更优雅但改变行为”的重构。字段值、状态码、方向/开平映射都要以兼容性为先。

## 构建与安装

- 安装依赖并构建包：
  `pip install .`

- 如需开发态安装：
  `pip install -e .`

- 构建后端是 `meson-python`，依赖 `meson>=1.7.0` 和 `pybind11>=2.13.6`。

- 当前 `meson.build` 里的扩展编译逻辑只在 Windows 分支下启用。不要假设 Linux 源码安装一定能直接编译成功；如果任务涉及 Linux 构建，先核对现有构建路径再改。

## 常用检查

仓库里没有现成的自动化测试目录，修改后优先做这些低风险检查：

- 语法检查：
  `python -m compileall vnpy_esunny script`

- 静态检查：
  `ruff check .`

- 类型检查：
  `mypy vnpy_esunny`

- 手工联调：
  `python script/run.py`

最后一项依赖本地已安装 `vnpy`/GUI 环境，以及实际可用的易盛柜台连接参数。

## 修改建议

- 改 Python 网关逻辑时，先看 `EsunnyGateway`、`QuoteApi`、`TradeApi` 三层调用链，不要只改单个回调。
- 改 C++ 扩展时，优先确认对应头文件签名、pybind 暴露和 Python 调用点是否一致。
- 如果需求涉及“接口字段缺失”“回调结构变化”“常量新增”，先判断是手工补丁还是应该更新生成脚本。
- 提交前在说明里明确本次修改影响的是 Python 映射层、C++ 封装层，还是打包/构建层。
