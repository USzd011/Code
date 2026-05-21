# GitHub Models API调用指南

## 📊 GitHub Models当前可用模型

**查询时间**: 2026-04-28

**可用模型列表：**
1. `gpt-4o` - OpenAI最新模型
2. `gpt-4o-mini` - 轻量版
3. `Meta-Llama-3.1-405B-Instruct` - Meta开源大模型
4. `Meta-Llama-3.1-8B-Instruct` - Meta轻量版
5. `Cohere-embed-v3-english` - Cohere嵌入模型
6. `Cohere-embed-v3-multilingual` - Cohere多语言嵌入
7. `text-embedding-3-large` - OpenAI嵌入模型
8. `text-embedding-3-small` - OpenAI轻量嵌入

---

## ❌ GPT-5不可用

**当前状态**: GitHub Models **不支持GPT-5**

**原因**:
- GPT-5尚未正式发布
- GitHub Models目前只提供GPT-4o系列

---

## ✅ 如何调用GitHub Models API

### 1. API端点

**基础URL**: `https://models.inference.ai.azure.com`

**聊天补全**: `https://models.inference.ai.azure.com/chat/completions`

**模型列表**: `https://models.inference.ai.azure.com/models`

---

### 2. 认证方式

**需要GitHub Personal Access Token**

**权限要求**: `models:read`

**我们的Token**: `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`

---

### 3. 调用示例

#### Python调用
```python
import requests

# API配置
api_url = "https://models.inference.ai.azure.com/chat/completions"
api_key = "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"

# 请求数据
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4o",  # 使用gpt-4o（当前最强）
    "messages": [
        {"role": "user", "content": "你好"}
    ]
}

# 发送请求
response = requests.post(api_url, headers=headers, json=data)
result = response.json()

print(result['choices'][0]['message']['content'])
```

#### cURL调用
```bash
curl -X POST "https://models.inference.ai.azure.com/chat/completions" \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

#### 使用我们的代理脚本
```bash
/root/.openclaw/workspace/api-proxy/ai_call.sh -m gpt-4o "你的问题"
```

---

### 4. 推荐模型

**最强模型**: `gpt-4o`
- 最新OpenAI模型
- 支持多模态
- 高质量输出

**快速模型**: `gpt-4o-mini`
- 速度快
- 成本低
- 适合简单任务

**开源模型**: `Meta-Llama-3.1-405B-Instruct`
- Meta最新开源
- 405B参数
- 免费使用

---

### 5. 速率限制

**免费额度**:
- 每分钟请求: 限制
- 每日请求: 限制
- Token限制: 限制

**建议**:
- 使用gpt-4o-mini节省配额
- 批量请求时注意间隔
- 遇到限制时等待重试

---

### 6. 实例ID/API ID

**模型ID就是模型名称**:
- `gpt-4o`
- `gpt-4o-mini`
- `Meta-Llama-3.1-405B-Instruct`

**无需额外的实例ID**，直接使用模型名称即可。

---

## 🎯 总结

**GPT-5状态**: ❌ 不可用

**推荐替代**:
- `gpt-4o` - 当前最强
- `gpt-4o-mini` - 快速轻量

**API地址**: `https://models.inference.ai.azure.com/chat/completions`

**认证方式**: Bearer Token

**立即可用**: ✅ 已配置Token

---

**使用我们的代理脚本快速调用：**
```bash
/root/.openclaw/workspace/api-proxy/ai_call.sh -m gpt-4o "问题"
```