# 网页AI平台技能封装方案

## 🎯 目标
将网页版AI平台封装成OpenClaw技能，通过浏览器自动化操作，无需API，直接搬运结果。

---

## 📋 可封装的网页平台

### 1. LMArena
- **地址**: https://lmarena.ai
- **特点**: 多模型对比测评
- **封装方式**: 浏览器自动化 → 输入问题 → 获取多个模型回答 → 返回结果

### 2. XSimple Chat
- **地址**: https://xsimplechat.com/chat
- **特点**: 聚合多模型对话
- **封装方式**: 浏览器自动化 → 输入问题 → 获取回答 → 返回结果

### 3. 蓝镜ChatGPT中文版
- **地址**: https://ai.lanjingchat.com
- **特点**: 中文友好
- **封装方式**: 浏览器自动化 → 输入问题 → 获取回答 → 返回结果

### 4. Gemini 官网
- **地址**: https://gemini.google.com
- **特点**: Gemini对话界面
- **封装方式**: 浏览器自动化 → 输入问题 → 获取回答 → 返回结果

---

## 🔧 技能实现方案

### 方案1：使用OpenClaw browser工具

```yaml
# skills/web-ai-platforms/SKILL.md
---
name: web-ai-platforms
description: 网页AI平台技能，通过浏览器自动化操作获取AI回答
---

## 使用方法

### LMArena对比测评
```
使用 lmarena 对比以下问题：[你的问题]
```

### XSimple Chat对话
```
使用 xsimplechat 回答：[你的问题]
```

### 蓝镜ChatGPT对话
```
使用 lanjingchat 回答：[你的问题]
```

### Gemini对话
```
使用 gemini 回答：[你的问题]
```
```

### 方案2：具体实现脚本

#### LMArena技能
```python
# skills/web-ai-platforms/scripts/lmarena.py
"""
LMArena多模型对比技能
通过浏览器自动化操作获取多个模型的回答
"""

def call_lmarena(prompt):
    """
    调用LMArena获取多模型对比结果
    
    步骤：
    1. 打开 https://lmarena.ai
    2. 找到输入框
    3. 输入问题
    4. 点击发送
    5. 等待响应
    6. 提取所有模型的回答
    7. 返回结果
    """
    # 使用OpenClaw browser工具
    # 1. 打开页面
    browser.open("https://lmarena.ai")
    
    # 2. 找到输入框并输入
    browser.type("input[placeholder='Enter your prompt']", prompt)
    
    # 3. 点击发送
    browser.click("button[type='submit']")
    
    # 4. 等待响应
    browser.wait(5)
    
    # 5. 提取所有模型的回答
    responses = browser.extract_all(".model-response")
    
    return responses
```

#### XSimple Chat技能
```python
# skills/web-ai-platforms/scripts/xsimplechat.py
"""
XSimple Chat对话技能
"""

def call_xsimplechat(prompt, model=None):
    """
    调用XSimple Chat
    
    步骤：
    1. 打开 https://xsimplechat.com/chat
    2. 选择模型（可选）
    3. 输入问题
    4. 获取回答
    """
    browser.open("https://xsimplechat.com/chat")
    
    # 选择模型
    if model:
        browser.click(f"[data-model='{model}']")
    
    # 输入问题
    browser.type("textarea", prompt)
    browser.click("button[type='submit']")
    
    # 等待响应
    browser.wait(3)
    
    # 提取回答
    response = browser.extract(".response-text")
    
    return response
```

#### 蓝镜ChatGPT技能
```python
# skills/web-ai-platforms/scripts/lanjingchat.py
"""
蓝镜ChatGPT中文版技能
"""

def call_lanjingchat(prompt):
    """
    调用蓝镜ChatGPT
    
    步骤：
    1. 打开 https://ai.lanjingchat.com
    2. 输入问题
    3. 获取回答
    """
    browser.open("https://ai.lanjingchat.com")
    
    # 输入问题
    browser.type("input[type='text']", prompt)
    browser.click("button[type='submit']")
    
    # 等待响应
    browser.wait(3)
    
    # 提取回答
    response = browser.extract(".chat-response")
    
    return response
```

---

## 🎯 技能触发规则

```yaml
# skills/web-ai-platforms/SKILL.md

## 触发示例

<example>
Context: 用户想要对比多个模型的回答
user: "使用LMArena对比：什么是人工智能？"
assistant: 我将使用LMArena获取多个模型的对比回答
<commentary>
触发 lmarena 技能，打开网页获取对比结果
</commentary>
</example>

<example>
Context: 用户想要快速对话
user: "用蓝镜ChatGPT回答：写一段Python代码"
assistant: 我将使用蓝镜ChatGPT获取回答
<commentary>
触发 lanjingchat 技能，打开网页获取结果
</commentary>
</example>
```

---

## 📊 优势对比

### 网页封装 vs API调用

| 方面 | 网页封装 | API调用 |
|------|----------|----------|
| 需要API Key | ❌ 不需要 | ✅ 需要 |
| 免费额度 | ✅ 无限制 | ⚠️ 有限制 |
| 稳定性 | ⚠️ 依赖网页 | ✅ 稳定 |
| 速度 | ⚠️ 较慢 | ✅ 快速 |
| 功能 | ✅ 完整功能 | ⚠️ 受限 |

---

## 🚀 实施步骤

### Step 1：创建技能目录
```bash
mkdir -p /root/.openclaw/workspace/skills/web-ai-platforms/scripts
```

### Step 2：创建SKILL.md
```bash
# 定义技能说明和触发规则
```

### Step 3：实现各平台脚本
```bash
# lmarena.py
# xsimplechat.py
# lanjingchat.py
# gemini.py
```

### Step 4：测试技能
```bash
# 测试各平台是否可用
```

---

## 💡 使用示例

### 在对话中使用

**用户**：使用LMArena对比一下Python和JavaScript的区别

**助手**：
```
我将使用LMArena获取多个模型的对比回答...

[打开浏览器]
[输入问题]
[获取结果]

模型A回答：...
模型B回答：...
模型C回答：...
```

---

## ⚠️ 注意事项

1. **网页变化**：网站更新可能导致技能失效
2. **速度较慢**：浏览器操作比API慢
3. **资源占用**：需要启动浏览器
4. **并发限制**：不适合高并发场景

---

## 🎯 下一步

**需要我立即开始实施吗？**

我可以：
1. 创建技能目录结构
2. 实现LMArena技能
3. 实现其他平台技能
4. 测试技能可用性
