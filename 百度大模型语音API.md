# 百度大模型语音API调用指南

> 整理时间: 2026-04-30
> 状态: 已开通，免费额度可用

## 🎯 可用服务

### 1. 大模型声音复刻
- **功能**: 创建自定义音色
- **免费额度**: 10/10次
- **状态**: ✅ 免费使用中

### 2. 大模型在线合成
- **功能**: 文字转语音
- **免费额度**: 5万字符
- **状态**: ✅ 免费使用中

### 3. 端到端语音语言大模型（Lite）
- **功能**: 实时语音交互
- **免费额度**: 500千tokens
- **状态**: ✅ 免费使用中

### 4. 端到端语音语言大模型（Pro）
- **功能**: 高级语音交互
- **免费额度**: 500千tokens
- **状态**: ✅ 免费使用中

### 5. 搜索增强
- **功能**: 语音搜索增强
- **免费额度**: 1000次
- **状态**: ✅ 免费使用中

---

## 🔧 API调用方式

### 鉴权方式

**获取Access Token**:
```python
import requests

def get_access_token(api_key, secret_key):
    url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={api_key}&client_secret={secret_key}&grant_type=client_credentials"
    response = requests.post(url)
    return response.json()['access_token']

# 使用示例
api_key = "XROJ8C1vKdivykji4rFq0jiE"
secret_key = "95pkHNbWf7VXSohszb8mvHPCd8wNmTCg"
access_token = get_access_token(api_key, secret_key)
```

---

## 🎤 语音合成（TTS）

### 短文本在线合成

**接口**: `https://tsn.baidu.com/text2audio`

**参数**:
| 参数 | 说明 |
|------|------|
| tex | 要合成的文本 |
| tok | Access Token |
| cuid | 客户端ID |
| ctp | 客户端类型（1） |
| lan | 语言（zh） |
| spd | 语速（0-15） |
| pit | 音调（0-15） |
| vol | 音量（0-15） |
| per | 发音人（0-4） |

**Python示例**:
```python
def text_to_speech(text, access_token):
    url = f"https://tsn.baidu.com/text2audio"
    params = {
        'tex': text,
        'tok': access_token,
        'cuid': '001',
        'ctp': 1,
        'lan': 'zh',
        'spd': 5,
        'pit': 5,
        'vol': 5,
        'per': 0  # 0=女声, 1=男声, 3=情感合成, 4=情感合成
    }
    response = requests.get(url, params=params)
    
    if 'audio' in response.headers.get('Content-Type', ''):
        with open('output.mp3', 'wb') as f:
            f.write(response.content)
        return True
    return False
```

---

## 🎧 语音识别（ASR）

### 短语音识别

**接口**: `https://vop.baidu.com/server_api`

**参数**:
| 参数 | 说明 |
|------|------|
| format | 音频格式（pcm/wav/amr） |
| rate | 采样率（16000） |
| channel | 声道数（1） |
| cuid | 客户端ID |
| token | Access Token |
| speech | 音频数据（base64） |
| len | 音频长度 |

**Python示例**:
```python
import base64

def speech_to_text(audio_file, access_token):
    url = "https://vop.baidu.com/server_api"
    
    with open(audio_file, 'rb') as f:
        audio_data = f.read()
    
    headers = {'Content-Type': 'application/json'}
    data = {
        'format': 'wav',
        'rate': 16000,
        'channel': 1,
        'cuid': '001',
        'token': access_token,
        'speech': base64.b64encode(audio_data).decode(),
        'len': len(audio_data)
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

---

## 🤖 大模型实时语音交互

### 端到端语音语言大模型

**接口**: WebSocket连接

**功能**: 
- 语音输入 → 大模型理解 → 语音输出
- 毫秒级响应
- 超拟人对话

**特点**:
- 端到端处理
- 支持打断
- 情感表达
- 多轮对话

**调用方式**: 需要WebSocket连接，详见官方文档

---

## 📊 免费额度总结

| 服务 | 免费额度 | 状态 |
|------|---------|------|
| 语音合成 | 5万字符/月 | ✅ |
| 语音识别 | 领取后免费 | ✅ |
| 大模型语音Lite | 500千tokens | ✅ |
| 大模型语音Pro | 500千tokens | ✅ |
| 声音复刻 | 10次 | ✅ |
| 搜索增强 | 1000次 | ✅ |

---

## 🔑 已有凭证

**应用1**: 002
- AppID: 123113941
- API Key: XROJ8C1vKdivykji4rFq0jiE
- Secret Key: 95pkHNbWf7VXSohszb8mvHPCd8wNmTCg

**应用2**: 小龙虾语音助手
- AppID: 123114038
- API Key: 9qsie...
- Secret Key: uOCeI...

---

## 📚 官方文档

- 语音技术文档: https://ai.baidu.com/ai-doc/SPEECH/index.html
- API调试: 控制台 → API在线调试
- SDK下载: 控制台 → HTTP SDK

---

**整理人**: 小龙虾智能体
**更新时间**: 2026-04-30
