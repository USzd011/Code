# 🚀 API代理服务 - 团队使用指南

## ✅ 服务已就绪！

**团队成员可以立即使用！**

---

## 📡 快速使用

### 方法1：命令行调用（推荐）

```bash
# 基础调用
/root/.openclaw/workspace/api-proxy/ai_call.sh "你好"

# 指定模型
/root/.openclaw/workspace/api-proxy/ai_call.sh -m gpt-4o "写一段代码"

# 使用DeepSeek
/root/.openclaw/workspace/api-proxy/ai_call.sh -m DeepSeek-V3-0324 "解释什么是AI"

# 使用Llama 4
/root/.openclaw/workspace/api-proxy/ai_call.sh -m Llama-4-Scout-17B-16E-Instruct "你好"
```

### 方法2：直接curl调用

```bash
curl -X POST https://models.inference.ai.azure.com/chat/completions \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "你的问题"}]}'
```

---

## 🎯 可用模型

| 模型 | 特点 | 推荐场景 |
|------|------|----------|
| gpt-4o-mini | 快速、便宜 | 日常对话、简单任务 |
| gpt-4o | 高质量 | 复杂推理、代码生成 |
| DeepSeek-V3-0324 | 中文优化 | 中文对话、代码生成 |
| Llama-4-Scout-17B-16E-Instruct | 开源模型 | 多文档处理 |

---

## 📊 测试结果

**已测试通过：**
- ✅ gpt-4o-mini - Token使用: 36
- ✅ gpt-4o - Token使用: 53
- ✅ DeepSeek-V3-0324 - Token使用: 43
- ✅ Llama-4-Scout-17B-16E-Instruct - Token使用: 45

---

## 🐍 Python集成

```python
import requests

API_URL = "https://models.inference.ai.azure.com/chat/completions"
API_KEY = "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"

def call_ai(prompt, model="gpt-4o-mini"):
    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    })
    return response.json()["choices"][0]["message"]["content"]

# 使用
result = call_ai("你好")
print(result)
```

---

## 📁 文件位置

**代理脚本**：
- `/root/.openclaw/workspace/api-proxy/ai_call.sh`

**配置文件**：
- `/root/.openclaw/workspace/llm_api_config.py`

**文档**：
- `/root/.openclaw/workspace/api-proxy/README.md`
- `/root/.openclaw/workspace/热门免费LLM-API清单.md`

---

## 💡 使用建议

**选择模型：**
- 快速响应 → gpt-4o-mini
- 高质量回答 → gpt-4o
- 中文优化 → DeepSeek-V3-0324
- 开源模型 → Llama-4-Scout-17B-16E-Instruct

**注意事项：**
- 注意频率限制
- 不要传输敏感数据
- 遵守使用条款

---

## 🚀 立即开始使用！

```bash
# 测试一下
/root/.openclaw/workspace/api-proxy/ai_call.sh "你好，请介绍一下GitHub Models"
```

**有问题随时反馈！** 🎉