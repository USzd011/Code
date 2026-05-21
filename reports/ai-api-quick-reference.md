# AI API 快速参考手册

> 生成时间: 2026-05-05
> 用途: 快速查阅各AI平台API调用方式

---

## OpenAI API

### 认证
```bash
# 环境变量
export OPENAI_API_KEY="sk-xxx"

# HTTP Header
Authorization: Bearer sk-xxx
```

### 对话补全
```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxx")

# 基础调用
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(response.choices[0].message.content)

# 流式输出
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

# 多模态 (图像输入)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": "https://..."}}
        ]
    }]
)

# 函数调用
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Beijing?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }]
)
```

### 图像生成
```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A serene lake at sunset",
    size="1024x1024",
    quality="standard",
    n=1
)
print(response.data[0].url)
```

### 语音识别
```python
with open("audio.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
print(transcript.text)
```

### 语音合成
```python
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello, this is a test."
)
response.stream_to_file("output.mp3")
```

### 向量嵌入
```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello world"
)
print(response.data[0].embedding)
```

### 可用模型
| 模型 | 用途 | 上下文 | 定价 (input/output per 1M tokens) |
|-----|------|--------|-----------------------------------|
| gpt-4o | 通用 | 128K | $2.5 / $10 |
| gpt-4o-mini | 轻量 | 128K | $0.15 / $0.6 |
| gpt-4-turbo | 高级推理 | 128K | $10 / $30 |
| gpt-3.5-turbo | 经济 | 16K | $0.5 / $1.5 |
| dall-e-3 | 图像生成 | - | $0.04-$0.12/image |
| whisper-1 | 语音识别 | - | $0.006/min |
| tts-1 | 语音合成 | - | $15/1M chars |

---

## Anthropic Claude API

### 认证
```bash
# 环境变量
export ANTHROPIC_API_KEY="sk-ant-xxx"

# HTTP Headers
x-api-key: sk-ant-xxx
anthropic-version: 2023-06-01
```

### 对话消息
```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-xxx")

# 基础调用
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)
print(message.content[0].text)

# 系统提示
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful coding assistant.",
    messages=[{"role": "user", "content": "Write a Python function"}]
)

# 流式输出
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# 多模态 (图像)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "url", "url": "https://..."}},
            {"type": "text", "text": "Describe this image"}
        ]
    }]
)

# 工具调用
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What's the weather?"}],
    tools=[{
        "name": "get_weather",
        "description": "Get weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }]
)
```

### 可用模型
| 模型 | 用途 | 上下文 | 定价 (input/output per 1M tokens) |
|-----|------|--------|-----------------------------------|
| claude-3-5-sonnet-20241022 | 通用/代码 | 200K | $3 / $15 |
| claude-3-5-haiku-20241022 | 快速响应 | 200K | $0.8 / $4 |
| claude-3-opus-20240229 | 高级推理 | 200K | $15 / $75 |

---

## Google Gemini API

### 认证
```bash
# 环境变量
export GOOGLE_API_KEY="AIza-xxx"

# 或使用 gcloud CLI
gcloud auth application-default login
```

### 对话生成
```python
import google.generativeai as genai

genai.configure(api_key="AIza-xxx")

# 创建模型
model = genai.GenerativeModel('gemini-2.0-flash')

# 基础调用
response = model.generate_content("Hello!")
print(response.text)

# 流式输出
response = model.generate_content("Tell me a story", stream=True)
for chunk in response:
    print(chunk.text, end="")

# 多轮对话
chat = model.start_chat(history=[])
response = chat.send_message("Hello!")
print(response.text)
response = chat.send_message("What did I just say?")
print(response.text)

# 系统指令
model = genai.GenerativeModel(
    'gemini-2.0-flash',
    system_instruction="You are a helpful coding assistant."
)

# 多模态
from PIL import Image
image = Image.open('image.jpg')
response = model.generate_content(["What's in this image?", image])

# 安全设置
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
]
response = model.generate_content("Hello", safety_settings=safety_settings)
```

### 可用模型
| 模型 | 用途 | 上下文 | 定价 |
|-----|------|--------|------|
| gemini-2.0-flash | 快速响应 | 1M | 免费额度 + $0.1/1M |
| gemini-1.5-pro | 高级推理 | 2M | $1.25 / $5 |
| gemini-1.5-flash | 轻量 | 1M | 免费额度 + $0.075/1M |
| gemini-embedding | 向量嵌入 | - | 免费额度 |

### 免费额度
- Gemini 2.0 Flash: 1500 RPD (requests per day)
- Gemini 1.5 Flash: 1500 RPD
- Gemini 1.5 Pro: 50 RPD

---

## DeepSeek API

### 认证
```bash
export DEEPSEEK_API_KEY="sk-xxx"
```

### 对话补全 (OpenAI兼容)
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxx",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Hello!"}]
)

# DeepSeek-Coder (代码专用)
response = client.chat.completions.create(
    model="deepseek-coder",
    messages=[{"role": "user", "content": "Write a Python function"}]
)
```

### 可用模型
| 模型 | 用途 | 上下文 | 定价 (input/output per 1M tokens) |
|-----|------|--------|-----------------------------------|
| deepseek-chat | 通用对话 | 64K | $0.14 / $0.28 |
| deepseek-coder | 代码生成 | 16K | $0.14 / $0.28 |

---

## GitHub Models API

### 认证
```bash
export GITHUB_TOKEN="ghp_xxx"
```

### 多模型调用 (OpenAI兼容)
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key="ghp_xxx"
)

# GPT-4o
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Claude 3.5 Sonnet
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Llama 4
response = client.chat.completions.create(
    model="llama-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# DeepSeek-V3
response = client.chat.completions.create(
    model="deepseek-v3",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 可用模型
- gpt-4o
- gpt-4.1
- claude-3-5-sonnet-20241022
- llama-4
- deepseek-v3
- mistral-large

### 免费额度
- 每个模型: 数千次请求/天
- 适合开发和测试

---

## 统一调用封装

### Python SDK
```python
from typing import Optional, Dict, Any
import os

class UnifiedAIClient:
    """统一AI API客户端"""
    
    def __init__(self):
        self.providers = {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": "https://api.openai.com/v1"
            },
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "base_url": "https://api.anthropic.com/v1"
            },
            "gemini": {
                "api_key": os.getenv("GOOGLE_API_KEY"),
                "base_url": "https://generativelanguage.googleapis.com/v1"
            },
            "deepseek": {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "base_url": "https://api.deepseek.com/v1"
            },
            "github": {
                "api_key": os.getenv("GITHUB_TOKEN"),
                "base_url": "https://models.inference.ai.azure.com"
            }
        }
    
    def chat(
        self,
        message: str,
        provider: str = "gemini",
        model: Optional[str] = None,
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """统一对话接口"""
        
        # 默认模型映射
        default_models = {
            "openai": "gpt-4o",
            "anthropic": "claude-3-5-sonnet-20241022",
            "gemini": "gemini-2.0-flash",
            "deepseek": "deepseek-chat",
            "github": "gpt-4o"
        }
        
        model = model or default_models.get(provider)
        
        if provider == "gemini":
            return self._chat_gemini(message, model, system, **kwargs)
        elif provider == "anthropic":
            return self._chat_anthropic(message, model, system, **kwargs)
        else:
            return self._chat_openai_compatible(message, model, provider, system, **kwargs)
    
    def _chat_gemini(self, message: str, model: str, system: Optional[str], **kwargs) -> str:
        import google.generativeai as genai
        genai.configure(api_key=self.providers["gemini"]["api_key"])
        
        model_obj = genai.GenerativeModel(
            model,
            system_instruction=system
        )
        response = model_obj.generate_content(message, **kwargs)
        return response.text
    
    def _chat_anthropic(self, message: str, model: str, system: Optional[str], **kwargs) -> str:
        import anthropic
        client = anthropic.Anthropic(api_key=self.providers["anthropic"]["api_key"])
        
        response = client.messages.create(
            model=model,
            max_tokens=kwargs.get("max_tokens", 1024),
            system=system,
            messages=[{"role": "user", "content": message}]
        )
        return response.content[0].text
    
    def _chat_openai_compatible(self, message: str, model: str, provider: str, system: Optional[str], **kwargs) -> str:
        from openai import OpenAI
        
        config = self.providers[provider]
        client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

# 使用示例
client = UnifiedAIClient()

# 使用Gemini (免费)
response = client.chat("Hello!", provider="gemini")

# 使用Claude (代码任务)
response = client.chat("Write a Python function", provider="anthropic")

# 使用DeepSeek (性价比)
response = client.chat("Explain quantum computing", provider="deepseek")

# 使用GitHub Models (免费多模型)
response = client.chat("Hello!", provider="github", model="claude-3-5-sonnet-20241022")
```

---

## 错误处理最佳实践

```python
import time
from typing import Optional

def robust_chat(
    message: str,
    providers: list = ["gemini", "deepseek", "openai"],
    max_retries: int = 3
) -> Optional[str]:
    """带降级和重试的健壮调用"""
    
    client = UnifiedAIClient()
    
    for provider in providers:
        for attempt in range(max_retries):
            try:
                return client.chat(message, provider=provider)
            except Exception as e:
                print(f"Provider {provider} failed (attempt {attempt+1}): {e}")
                time.sleep(2 ** attempt)  # 指数退避
        
        print(f"Provider {provider} exhausted, trying next...")
    
    return None
```

---

_快速参考手册生成完毕_