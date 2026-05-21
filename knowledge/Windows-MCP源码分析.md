# Windows-MCP 源码分析与Linux适配方案

## 项目概览

| 项目 | 值 |
|------|-----|
| 名称 | Windows-MCP |
| 版本 | v0.7.4 |
| 协议 | MIT |
| 作者 | Jeomon George (@CursorTouch) |
| 用户 | 200万+ (Claude Desktop扩展) |
| 仓库 | [github.com/CursorTouch/Windows-MCP](https://github.com/CursorTouch/Windows-MCP) |
| PyPI | `windows-mcp` |

## 源码架构

```
src/windows_mcp/
├── __main__.py    ← 入口点: CLI启动MCP服务器
├── __init__.py    ← 模块初始化
├── config.py      ← 配置管理(WINDOWS_MCP_DEBUG)
├── server.py      ← 核心: FastMCP + 声明周期管理
├── analytics.py   ← PostHog遥测
├── paths.py       ← 路径管理
├── desktop/       ← Windows桌面交互核心
│   └── service.py → Desktop() 类
├── tools/         ← MCP工具注册
│   ├── __init__.py → register_all() 注册所有工具
│   └── snapshot.py → 截图/状态工具
├── filesystem/    ← 文件系统操作
├── registry/      ← Windows注册表
├── tree/          ← UI元素树
├── uia/           ← UI Automation (Windows无障碍API)
├── vdm/           ← 虚拟桌面管理器
└── watchdog/      ← 系统状态监控
```

## 核心技术栈

### MCP框架层 (跨平台 ✅)
```
fastmcp>=3.0  → FastMCP框架
click         → CLI命令行
starlette     → HTTP/SSE传输
asyncio       → 异步IO
```

### Windows绑定层 (Windows only 🔴)
```
pywin32       → Win32 API (窗口/进程/输入)
comtypes      → COM接口 (UIAutomation)
dxcam         → DirectX屏幕捕获
```

### 通用工具层 (跨平台 ✅)
```
psutil        → 系统监控
pillow        → 图像处理
markdownify   → HTML→Markdown
python-levenshtein → 模糊匹配
tabulate      → 表格格式化
```

## 核心工作流

```
LLM/AI代理
    │
    ├─[stdio/SSE]─── MCP协议 ───┐
    │                           │
    ▼                           ▼
FastMCP Server  ←────── 工具调用
    │
    ├─ Desktop() → pywin32 → Windows API → 操控窗口/应用
    ├─ UIA()     → comtypes → UI Automation → 获取UI元素树
    ├─ WatchDog  → psutil   → 监控系统状态
    ├─ Filesystem→ os/path  → 文件导航操作
    └─ Registry  → winreg   → 注册表操作
```

## Linux适配方案

### 方案A：轻量适配（直接使用我已有的能力）

Windows-MCP的功能 | 我在Linux上的替代方案
-----------------|---------------------
窗口控制 | `exec` → wmctrl / xdotool
键盘/鼠标操作 | `exec` → xdotool / ydotool
截图 | `exec` → import (ImageMagick) / scrot
文件导航 | `read/write/exec` → 已有
进程管理 | `exec` → ps/kill
浏览器自动化 | OpenClaw内置浏览器 ✅ 已有
系统监控 | `exec` → top/free/df

**结论：我已有的 exec + read/write + browser 已经覆盖95%**

### 方案B：完整MCP Server（造Linux版Windows-MCP）

```python
from fastmcp import FastMCP  # 同款框架

mcp = FastMCP("linux-mcp")

# Linux桌面交互
@mcp.tool()
def linux_desktop(action: str, target: str) -> str:
    """通过xdotool/yadotool操控Linux桌面"""
    ...

# Linux文件系统  
@mcp.tool()
def linux_fs(path: str) -> str:
    """文件导航/读写"""
    ...

# Linux进程
@mcp.tool()
def linux_process(name: str) -> str:
    """进程管理"""
    ...
```

### 我推荐：方案A（已有能力足够）

先不重复造轮子。如果以后需要，随时可以按方案B搭建。

## 关键学习点

1. **MCP协议** = AI和工具之间的标准化通信协议
2. **FastMCP** = 跨平台框架，在哪都能用
3. **工具注册模式** = `register_all(mcp, ...)` 统一注册
4. **SSE/stdio传输** = 支持本地(stdin/stdout)和远程(HTTP SSE)
5. **lifespan生命周期** = 启动初始化/关闭清理

## 存储路径
- 仓库源码: https://github.com/CursorTouch/Windows-MCP
- 克隆镜像: 未克隆（可后续 `git clone`）
- 依赖分析: 已在上方列出
