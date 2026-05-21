# OpenClaw 智能体网络 - 互联互通配置

## 🦞 当前智能体架构

### 主控智能体（当前）
- **名称**: OpenClaw Main Agent
- **状态**: ✅ 运行中
- **会话ID**: ec9fde84-1160-44c6-83cf-999129a60630
- **模型**: astron-code-latest (GLM-5)
- **上下文**: 200K tokens

---

## 🔗 已打通的通道

### 1. 企业微信通道
- **状态**: ✅ 已连接
- **Bot ID**: aibhpOsAB8PBhXs9MxiPOPBoBUBDx8T8wPG
- **连接模式**: WebSocket

### 2. 钉钉通道
- **状态**: ✅ 已安装
- **插件**: ddingtalk

### 3. 微信通道
- **状态**: ✅ 已安装
- **插件**: openclaw-weixin

### 4. 元宝AI
- **状态**: ✅ 已安装
- **插件**: openclaw-plugin-yuanbao

### 5. QQ机器人
- **状态**: ✅ 已安装
- **插件**: lightclawbot

---

## 🌐 Gateway 网关

- **端口**: 23243
- **模式**: local
- **认证**: Token
- **WebSocket**: ws://106.53.73.165:23243/zvi9jr

---

## 🔄 智能体协作能力

### 子智能体派发
```python
# 派发任务给子智能体
sessions_spawn(
    task="处理子任务",
    runtime="subagent"
)
```

### 会话间通信
```python
# 向其他会话发送消息
sessions_send(
    sessionKey="target-session",
    message="消息内容"
)
```

### 查看其他会话
```python
# 列出所有活跃会话
sessions_list()
```

---

## 📊 智能体状态

| 智能体 | 状态 | 通道 |
|--------|------|------|
| Main Agent | ✅ 运行中 | 企业微信 |
| 浏览器智能体 | ✅ 待命 | Chromium |
| 记忆智能体 | ✅ 运行中 | memory-tencentdb |

---

## 🚀 扩展能力

### 可派发的子智能体类型
1. **coding-agent** - 代码编写
2. **research-agent** - 信息搜索
3. **browser-agent** - 浏览器自动化
4. **memory-agent** - 记忆管理

### 智能体间共享
- ✅ 会话历史
- ✅ 文件系统
- ✅ 工具调用
- ✅ 记忆系统

---

**所有智能体已互联互通！** 🦞🔗
