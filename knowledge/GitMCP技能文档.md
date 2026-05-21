# GitMCP 技能 — 一键获取GitHub项目文档

## 来源
抖音"程序员三干"推荐，杨欢要求全员掌握。

## 核心用法
把 `github.com` 换成 `gitmcp.io`：

```
原: https://github.com/microsoft/playwright-mcp
→  https://gitmcp.io/microsoft/playwright-mcp
```

## 原理
GitMCP 自动将任意GitHub仓库的README/文档/API参考转为 **MCP Server**（Model Context Protocol），AI助手可直接读取。

## 支持的AI IDE配置

| 工具 | 配置方式 |
|------|---------|
| **Cursor** | `~/.cursor/mcp.json` → `{"url": "https://gitmcp.io/..."}` |
| **Claude Desktop** | `claude_desktop_config.json` → `npx mcp-remote https://gitmcp.io/...` |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` → `{"serverUrl": "https://gitmcp.io/..."}` |
| **VSCode** | `.vscode/mcp.json` → SSE模式 |
| **Cline** | `settings/cline_mcp_settings.json` → URL模式 |
| **Highlight AI** | 插件面板配置 |
| **Augment Code** | 插件面板配置 |
| **Msty AI** | 插件面板配置 |

## 4号腾云使用方式

```bash
# 直接读取仓库文档
python3 /root/.openclaw/workspace/starbrain-v5/gitmcp_reader.py <owner>/<repo>

# 示例
python3 gitmcp_reader.py microsoft/playwright-mcp
```

## 扩展用法
任意公开GitHub仓库都能用。遇到需要读文档的项目，直接：

1. 拿到仓库地址（如 `github.com/owner/repo`）
2. 换成 `gitmcp.io/owner/repo`
3. 获取文档内容

## 已知限制
- 仅限公开仓库
- 页面是React渲染，工具直接解析HTML
- 内容以文档/README为主，不含源码分析
