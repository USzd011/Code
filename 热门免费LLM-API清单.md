# 热门免费LLM API 快速调用清单

基于 cheahjs/free-llm-api-resources 项目，整理了5个最实用、门槛最低的免费API。

---

## 1. OpenRouter（聚合平台，新手首选）

✅ **优势**：聚合了30+免费模型，无需单独注册多平台，API格式兼容OpenAI

**免费额度**：
- 每分钟20次请求
- 每日50次请求（充值$10可升级到每日1000次）

**推荐模型**：
- `google/gemma-3-1b-it:free`
- `meta-llama/llama-3-8b-instruct:free`
- `mistralai/mistral-small-3.1:free`

**API地址**：`https://openrouter.ai/api/v1`

**调用示例（Python）**：
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="你的OpenRouter_API_KEY"
)

response = client.chat.completions.create(
    model="google/gemma-3-1b-it:free",
    messages=[{"role": "user", "content": "写一段Python快速排序代码"}]
)
print(response.choices[0].message.content)
```

---

## 2. Google AI Studio（Gemini系列，无信用卡）

✅ **优势**：Gemini模型免费额度高，支持长文本和多模态

**免费额度**：
- Gemini 3.1 Flash Lite：15请求/分钟，1500请求/天，上下文250k tokens

**推荐模型**：
- `gemini-3.1-flash-lite`
- `gemini-3.1-flash`（免费额度略低）

**API地址**：`https://generativelanguage.googleapis.com/v1beta`

**调用示例（Python）**：
```python
import google.generativeai as genai

genai.configure(api_key="你的Google_AI_Studio_KEY")
model = genai.GenerativeModel("gemini-3.1-flash-lite")
response = model.generate_content("解释一下什么是大语言模型")
print(response.text)
```

---

## 3. Groq（极速推理，高并发友好）

✅ **优势**：基于Llama 3/Mistral的极速推理，免费额度对开发测试非常友好

**免费额度**：
- 每分钟30请求
- 14400请求/天
- tokens限制约30k/分钟

**推荐模型**：
- `llama3-8b-8192`
- `mixtral-8x7b-32768`

**API地址**：`https://api.groq.com/openai/v1`

**调用示例（Python）**：
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="你的Groq_API_KEY"
)

response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": "用Python写一个快速排序算法"}]
)
print(response.choices[0].message.content)
```

---

## 4. NVIDIA NIM（企业级模型，无信用卡）

✅ **优势**：NVIDIA提供的开源模型服务，支持Llama 3、Nemotron等模型，延迟低

**免费额度**：
- 部分模型永久免费
- 速率限制约每分钟10-20请求

**推荐模型**：
- `meta/llama3-8b-instruct`
- `nvidia/nemotron-mini-4b-instruct`

**API地址**：`https://integrate.api.nvidia.com/v1`

**调用示例（Python）**：
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="你的NVIDIA_API_KEY"
)

response = client.chat.completions.create(
    model="meta/llama3-8b-instruct",
    messages=[{"role": "user", "content": "写一段简单的Python爬虫代码"}]
)
print(response.choices[0].message.content)
```

---

## 5. Mistral AI（官方免费层，轻量模型）

✅ **优势**：Mistral官方提供的免费API，模型轻量高效，适合快速原型开发

**免费额度**：
- 每分钟20请求
- 1000请求/天

**推荐模型**：
- `mistral-small-3.1`
- `mistral-7b-instruct-v0.3`

**API地址**：`https://api.mistral.ai/v1`

**调用示例（Python）**：
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.mistral.ai/v1",
    api_key="你的Mistral_API_KEY"
)

response = client.chat.completions.create(
    model="mistral-small-3.1",
    messages=[{"role": "user", "content": "解释什么是API接口"}]
)
print(response.choices[0].message.content)
```

---

## ⚠️ 关键使用注意事项

1. **额度与限制**：免费服务均有速率/请求/Token限制，仅适合原型开发、学习测试，不建议直接用于生产环境
2. **合规使用**：请遵守各平台的服务条款，避免滥用导致免费额度被封禁
3. **地区限制**：部分服务可能需要科学上网或境外手机号注册，使用前请确认地区支持
4. **安全风险**：请勿在免费API中传输敏感数据，避免数据泄露

---

## 📌 快速上手建议

- **新手优先选 OpenRouter**：一次注册就能用30+免费模型，兼容OpenAI格式，学习成本最低
- **追求速度选 Groq**：推理延迟极低，适合需要快速响应的测试场景
- **长文本/多模态测试选 Google AI Studio**：Gemini的免费额度对长上下文支持更好

---

## ✅ 已配置可用

### GitHub Models（已测试通过）
- **Token**: `[REDACTED]`
- **API**: `https://models.inference.ai.azure.com/chat/completions`
- **可用模型**: GPT-4o, DeepSeek-V3, Llama 4等
- **状态**: ✅ 立即可用
