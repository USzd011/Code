# 统一LLM API配置文件
# 直接替换API Key就能切换不同服务商

# ============================================================
# 配置区域 - 只需修改这里
# ============================================================

# 当前使用的服务商（可选：openrouter, google, groq, nvidia, mistral, github）
CURRENT_PROVIDER = "github"

# API Keys（替换为你的实际Key）
API_KEYS = {
    "openrouter": "你的OpenRouter_API_KEY",
    "google": "你的Google_AI_Studio_KEY",
    "groq": "你的Groq_API_KEY",
    "nvidia": "你的NVIDIA_API_KEY",
    "mistral": "你的Mistral_API_KEY",
    "github": "[GITHUB_TOKEN]"  # ✅ 已配置
}

# 服务商配置
PROVIDERS = {
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "google/gemma-3-1b-it:free",
        "models": ["google/gemma-3-1b-it:free", "meta-llama/llama-3-8b-instruct:free"]
    },
    "google": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "default_model": "gemini-3.1-flash-lite",
        "models": ["gemini-3.1-flash-lite", "gemini-3.1-flash"]
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "llama3-8b-8192",
        "models": ["llama3-8b-8192", "mixtral-8x7b-32768"]
    },
    "nvidia": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "default_model": "meta/llama3-8b-instruct",
        "models": ["meta/llama3-8b-instruct", "nvidia/nemotron-mini-4b-instruct"]
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "default_model": "mistral-small-3.1",
        "models": ["mistral-small-3.1", "mistral-7b-instruct-v0.3"]
    },
    "github": {
        "base_url": "https://models.inference.ai.azure.com",
        "default_model": "gpt-4o-mini",
        "models": ["gpt-4o-mini", "gpt-4o", "DeepSeek-V3-0324", "Llama-4-Scout-17B-16E-Instruct"]
    }
}

# ============================================================
# 使用示例 - 无需修改
# ============================================================

# Python 示例
"""
from openai import OpenAI

# 自动选择当前配置的服务商
provider = PROVIDERS[CURRENT_PROVIDER]
client = OpenAI(
    base_url=provider["base_url"],
    api_key=API_KEYS[CURRENT_PROVIDER]
)

# 调用API
response = client.chat.completions.create(
    model=provider["default_model"],
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
"""

# cURL 示例
"""
# GitHub Models (当前配置)
curl -X POST https://models.inference.ai.azure.com/chat/completions \
  -H "Authorization: Bearer [GITHUB_TOKEN]" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "你好"}]}'

# OpenRouter
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer 你的OpenRouter_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "google/gemma-3-1b-it:free", "messages": [{"role": "user", "content": "你好"}]}'

# Groq
curl -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer 你的Groq_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "你好"}]}'
"""

# Node.js 示例
"""
const { OpenAI } = require('openai');

const provider = PROVIDERS[CURRENT_PROVIDER];
const client = new OpenAI({
  baseURL: provider.base_url,
  apiKey: API_KEYS[CURRENT_PROVIDER]
});

async function main() {
  const response = await client.chat.completions.create({
    model: provider.default_model,
    messages: [{ role: 'user', content: '你好' }]
  });
  console.log(response.choices[0].message.content);
}

main();
"""
