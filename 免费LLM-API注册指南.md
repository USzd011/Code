# 免费LLM API注册指南 - 团队共享资源

## ✅ 已注册成功

### 1. GitHub Models（推荐）
- **Token**: `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`
- **账号**: 13202924350@163.com
- **可用模型**:
  - GPT-5 (200k context, 100k output)
  - GPT-4.1 / GPT-4o / GPT-4o mini
  - DeepSeek-V3-0324
  - Llama 4 Scout 17B 16E Instruct
  - Llama 3.3 70B Instruct
  - Claude系列
  - Mistral系列
  - Phi-4系列
- **免费额度**: 有免费速率限制
- **API地址**: `https://models.inference.ai.azure.com`
- **使用方法**: 见下方代码示例

### 2. 讯飞星火RPA平台
- **密钥**: `tjFcggP30QFUq1m8cxeQaHV6UyRkvFH3`
- **API授权凭证**: `rze7t1f2fnRRcW1zCRxVnnrCTUWUm3c7`
- **账号**: 13202924350
- **密码**: xzc8769280

---

## 📋 待注册平台（需要手动完成）

### 3. HuggingFace
- **注册地址**: https://huggingface.co/join
- **账号**: 13202924350@163.com
- **密码**: xzc8769280YZH
- **免费额度**: $0.10/月
- **优势**: 国内可直接访问

### 4. Cloudflare Workers AI
- **注册地址**: https://dash.cloudflare.com/sign-up
- **账号**: 13202924350@163.com
- **密码**: xzc8769280YZH
- **免费额度**: 10,000 neurons/天
- **优势**: 国内可直接访问

### 5. Cohere
- **注册地址**: https://dashboard.cohere.com/welcome/register
- **账号**: 13202924350@163.com
- **密码**: xzc8769280YZH
- **免费额度**: 20请求/分钟，1000请求/月
- **注意**: 可能需要科学上网

---

## 🌐 需要科学上网的平台

### 6. Google AI Studio
- **注册地址**: https://aistudio.google.com/app/apikey
- **账号**: 13202924350@163.com
- **免费额度**: Gemini系列模型免费
- **注意**: 需要手机验证（+86可能不支持）

### 7. NVIDIA NIM
- **注册地址**: https://build.nvidia.com/
- **免费额度**: 40请求/分钟
- **注意**: 需要手机验证

### 8. Mistral
- **注册地址**: https://console.mistral.ai/
- **免费额度**: 1请求/秒，500k tokens/分钟
- **注意**: 需要手机验证

---

## 💻 使用示例

### GitHub Models API调用

```python
import requests
import json

# API配置
API_URL = "https://models.inference.ai.azure.com/chat/completions"
API_KEY = "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"

def call_gpt5(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-5",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

# 使用示例
result = call_gpt5("你好，请介绍一下自己")
print(result)
```

### Node.js调用示例

```javascript
const axios = require('axios');

const API_URL = 'https://models.inference.ai.azure.com/chat/completions';
const API_KEY = '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';

async function callModel(prompt, model = 'gpt-5') {
  const response = await axios.post(API_URL, {
    model: model,
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.7,
    max_tokens: 2000
  }, {
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data;
}

// 使用示例
callModel('你好，请介绍一下自己').then(console.log);
```

### cURL调用示例

```bash
curl -X POST https://models.inference.ai.azure.com/chat/completions \
  -H "Authorization: Bearer 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" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

---

## 📊 可用模型列表

### GitHub Models 支持的模型

| 模型 | Context | 特点 |
|------|---------|------|
| GPT-5 | 200k input, 100k output | 逻辑推理、多步骤任务 |
| GPT-4.1 | 1M input | 最新GPT-4版本 |
| GPT-4o | 128k input | 多模态、速度快 |
| DeepSeek-V3-0324 | 64k | 代码生成、推理能力强 |
| Llama 4 Scout | 128k | 多文档摘要、代码库推理 |
| Llama 3.3 70B | 128k | 开源模型，性能优秀 |
| Claude系列 | 200k | 长文本理解 |
| Mistral系列 | 32k | 欧洲开源模型 |

---

## ⚠️ 注意事项

1. **Token安全**: 不要将Token提交到公开仓库
2. **速率限制**: 免费额度有限，注意控制调用频率
3. **数据隐私**: 部分平台会使用数据进行训练
4. **地区限制**: 部分平台对中国IP有限制

---

## 🔄 更新日志

- 2026-04-28: GitHub Models注册成功
- 2026-04-28: 创建团队共享API资源库
