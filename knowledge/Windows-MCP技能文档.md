# Windows-MCP — AI操控Windows系统（全员必修 ⭐）

## 来源
抖音"AIGC前端老陈"推荐，杨欢标注"这个最重要"，要求全员掌握。

## 核心价值
**AI代理通过MCP协议直接操控Windows操作系统**，实现：
- 文件导航管理
- 应用控制启动
- UI界面交互点击
- QA自动化测试
- 浏览器自动化（DOM模式）

## 关键特性

| 特性 | 说明 |
|------|------|
| **任意LLM兼容** | 不依赖传统CV或微调模型，任何LLM都能用 |
| **UI自动化工具集** | 键盘/鼠标/窗口/状态捕捉全包含 |
| **实时交互** | 动作延迟0.2~0.5秒 |
| **轻量级开源** | 最小依赖，MIT许可，完整源码 |
| **可定制扩展** | 轻松调整或扩展工具 |
| **DOM模式** | 浏览器自动化专用模式，过滤浏览器UI元素 |

## 安装要求

```
平台: Windows 7~11
语言: Python 3.13+
包管理: UV (pip install uv)
安装: uvx windows-mcp
```

## 配置到AI IDE

### Claude Desktop
```json
{
  "mcpServers": {
    "windows-mcp": {
      "command": "uvx",
      "args": ["windows-mcp"]
    }
  }
}
```

### Cursor
在 `~/.cursor/mcp.json` 中添加：
```json
{
  "mcpServers": {
    "windows-mcp": {
      "command": "uvx",
      "args": ["windows-mcp"]
    }
  }
}
```

## 生态
- **用户规模**: Claude Desktop 扩展中200万+用户
- **独立Agent**: `windows-use`（基于Windows-MCP构建）
- **MCP Registry**: 已收录
- **PyPI**: 已发布 `windows-mcp`

## GitHub
- **仓库**: `CursorTouch/Windows-MCP`
- **协议**: MIT
- **Discord**: 社区活跃
- **更新**: 持续活跃（last commit today）

## 为什么最重要
杨欢说"这个最重要"——因为这正是突破口：
1. 番茄小说验证码突破 → Windows-MCP 可以直接操控Windows浏览器绕过自动化检测
2. 任何Windows自动化任务 → 从此AI可以直接操控Windows系统
3. 与GitMCP互补 → GitMCP读文档，Windows-MCP执行操作

## 参考链接
- GitHub: https://github.com/CursorTouch/Windows-MCP
- PyPI: https://pypi.org/project/windows-mcp/
- GitMCP文档: https://gitmcp.io/CursorTouch/Windows-MCP
- 抖音: AIGC前端老陈
