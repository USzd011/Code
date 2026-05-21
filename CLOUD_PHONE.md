# 云手机控制方案

## 扣子云设备信息

### 云手机
- 设备名称: `wkGkbAe78Q`
- 设备ID: `13657`
- 系统: Android
- 规格: 2vCPU | 6GB内存
- 屏幕: 1080×1920, 320dpi, 60fps
- 存储: 45GB (8.259GB可用)

### 云电脑
- 设备名称: `Yang`
- 设备ID: `14592`
- 系统: Ubuntu
- 规格: 标准版

## 控制方案

### 方案1: OpenClaw CloudPhone 插件（推荐）

**GitHub**: `@whateverai/cloudphone`

**功能**:
- 14个工具API（截图、点击、滑动、输入、开关机等）
- 自然语言操控云手机
- 任何Agent都能使用

**配置步骤**:
1. 注册 https://whateverai.ai 获取API Key
2. 在 openclaw.json 中配置 baseUrl 和 apikey
3. 执行 `openclaw plugins install @whateverai/cloudphone`

### 方案2: 火山引擎云手机 OpenAPI

**功能**:
- 实例管理
- ADB命令执行
- 应用安装
- 完整的REST API

**适用场景**:
- 自己搭建的智能体调用
- 需要更底层的控制

## 当前状态

- 扣子账号: 已登录
- 云手机: 空闲
- 云电脑: 空闲
- 手机号: 13202924350

## 下一步

1. 安装 `@whateverai/cloudphone` 插件
2. 配置API Key
3. 测试云手机控制
4. 登录快手/抖音

---

**更新时间**: 2026-05-02
