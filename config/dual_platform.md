# 双平台免费模型自动轮换配置

## 平台配置

### DMXAPI（国内优先）
- 接口地址: `https://www.dmxapi.cn/v1`
- API Key: `[REDACTED]`
- 免费模型:
  - `qwen3.5-35b-a3b-free`
  - `glm-4.7-flash-free`
  - `minimax-m2.7-free`
  - `mimo-v2-pro-free`

### OpenRouter（海外兜底）
- 接口地址: `https://openrouter.ai/api/v1`
- API Key: `[REDACTED]`
- 免费模型:
  - `google/gemini-flash-1.5:free`
  - `meta-llama/llama-3.1-8b-instruct:free`
  - `deepseek/deepseek-v3.2:free`

## 核心逻辑
1. **优先级**: DMXAPI（国内直连） → OpenRouter（海外兜底）
2. **自动兜底**: DMX 全失败自动切 OpenRouter
3. **全程免费**: 无需充值，零扣费
4. **功能**: 流式输出 + 多轮对话记忆 + 失败重试

## 状态
- ✅ 已记录
