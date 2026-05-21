# 讯飞开放平台 API 接口文档

> 整理时间: 2026-04-30
> 平台: 讯飞开放平台 https://www.xfyun.cn/

## 📋 已有账号信息

- **账号**: 13202924350
- **密码**: xzc8769280
- **APPID**: 需登录控制台查看
- **API Key**: 需登录控制台查看
- **API Secret**: 需登录控制台查看

---

## 🎤 语音类 API

### 1. 语音合成（TTS）- 在线语音合成

**接口地址**: `wss://tts-api.xfyun.cn/v2/tts`

**功能**: 将文字转换为语音

**请求方式**: WebSocket

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| text | string | 待合成文本（最大8192字节）|
| voice_name | string | 发音人（xiaoyan/aisjiuxu/aisxping等）|
| speed | int | 语速（0-100）|
| volume | int | 音量（0-100）|
| pitch | int | 音高（0-100）|

**发音人列表**:
- `xiaoyan` - 小燕（女声，亲和自然）
- `aisjiuxu` - 许久（男声，亲切）
- `aisxping` - 小萍（女声，温柔）
- `xiaoyan` - 小燕（默认）
- 更多发音人见控制台

**Python示例**:
```python
import websocket
import json
import base64
import hmac
import hashlib
from datetime import datetime
from urllib.parse import urlencode

def get_auth_url(api_key, api_secret, host, path, method="GET"):
    """生成鉴权URL"""
    now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature_origin = f"host: {host}\ndate: {now}\n{method} {path} HTTP/1.1"
    signature_sha = hmac.new(
        api_secret.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    signature = base64.b64encode(signature_sha).decode()
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()
    params = {"authorization": authorization, "date": now, "host": host}
    return f"wss://{host}{path}?{urlencode(params)}"

# 使用示例
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
auth_url = get_auth_url(api_key, api_secret, "tts-api.xfyun.cn", "/v2/tts")
```

---

### 2. 语音听写（ASR）- 流式语音识别

**接口地址**: `wss://iat-api.xfyun.cn/v2/iat`

**功能**: 将语音转换为文字

**请求方式**: WebSocket

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| audio | bytes | 音频数据（base64编码）|
| audio_status | int | 音频状态（0首帧/1中间帧/2尾帧）|
| encoding | string | 音频编码（raw/lame/speex）|
| sample_rate | int | 采样率（16000/8000）|

**Python示例**:
```python
import websocket
import json
import base64

def speech_to_text(audio_file_path, appid, api_key, api_secret):
    """语音识别"""
    # 生成鉴权URL（同TTS）
    auth_url = get_auth_url(api_key, api_secret, "iat-api.xfyun.cn", "/v2/iat")
    
    ws = websocket.create_connection(auth_url)
    
    # 发送音频数据
    with open(audio_file_path, 'rb') as f:
        audio_data = base64.b64encode(f.read()).decode()
    
    frame = {
        "common": {"app_id": appid},
        "business": {
            "language": "zh_cn",
            "domain": "iat",
            "accent": "mandarin"
        },
        "data": {
            "status": 2,
            "format": "audio/L16;rate=16000",
            "encoding": "raw",
            "audio": audio_data
        }
    }
    
    ws.send(json.dumps(frame))
    result = ws.recv()
    return json.loads(result)
```

---

### 3. 语音转写（长语音）

**接口地址**: `https://raasr.xfyun.cn/v2/api`

**功能**: 长音频（5小时以内）转文字

**适用场景**: 会议录音、课程录音、访谈录音

**特点**:
- 支持长音频（最长5小时）
- 异步处理，轮询获取结果
- 支持多说话人分离

---

### 4. 实时语音转写

**接口地址**: `wss://rtasr.xfyun.cn/v1/ws`

**功能**: 实时流式语音转写

**适用场景**: 直播字幕、会议实时记录

---

## 🖼️ 图像类 API

### 1. 通用文字识别 OCR

**接口地址**: `https://api.xfyun.cn/v1/service/v1/ocr/general`

**功能**: 识别图片中的文字

**请求方式**: HTTP POST

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| image | string | 图片base64编码 |
| location | string | 是否返回位置信息 |

**Python示例**:
```python
import requests
import base64
import hashlib
import time

def ocr_recognize(image_path, appid, api_key, api_secret):
    """通用文字识别"""
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()
    
    param = {"location": "false"}
    param_base64 = base64.b64encode(json.dumps(param).encode()).decode()
    
    timestamp = str(int(time.time()))
    signature_origin = f"host: api.xfyun.cn\ndate: {timestamp}\nPOST /v1/service/v1/ocr/general HTTP/1.1"
    signature = base64.b64encode(
        hmac.new(api_secret.encode(), signature_origin.encode(), hashlib.sha256).digest()
    ).decode()
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Appid": appid,
        "X-CurTime": timestamp,
        "X-Param": param_base64,
        "X-CheckSum": hashlib.md5((api_key + timestamp + param_base64).encode()).hexdigest()
    }
    
    data = {"image": image_data}
    response = requests.post(
        "https://api.xfyun.cn/v1/service/v1/ocr/general",
        headers=headers,
        data=data
    )
    return response.json()
```

---

### 2. 手写文字识别

**接口地址**: `https://api.xfyun.cn/v1/service/v1/ocr/handwriting`

**功能**: 识别手写文字

---

### 3. 身份证识别

**接口地址**: `https://api.xfyun.cn/v1/service/v1/ocr/idcard`

**功能**: 识别身份证正反面信息

---

### 4. 银行卡识别

**接口地址**: `https://api.xfyun.cn/v1/service/v1/ocr/bankcard`

**功能**: 识别银行卡号

---

### 5. 车牌识别

**接口地址**: `https://api.xfyun.cn/v1/service/v1/ocr/licenseplate`

**功能**: 识别车牌号码

---

### 6. 名片识别

**接口地址**: `https://api.xfyun.cn/v1/service/v1/ocr/businessCard`

**功能**: 识别名片信息

---

### 7. 增值税发票识别

**接口地址**: `https://api.xfyun.cn/v1/service/v1/ocr/vat_invoice`

**功能**: 识别增值税发票信息

---

### 8. 图像识别（场景识别）

**接口地址**: `https://api.xfyun.cn/v1/service/v1/image/identify`

**功能**: 识别图像中的物体、场景

---

### 9. 人脸检测与比对

**接口地址**: `https://api.xfyun.cn/v1/service/v1/face/detect`

**功能**:
- 人脸检测
- 人脸比对（1:1）
- 人脸搜索（1:N）
- 活体检测

---

## 🤖 星火大模型 API

### 星火认知大模型

**接口地址**: `wss://spark-api.xf-yun.com/v3.5/chat`

**功能**: 对话、写作、代码生成等

**模型版本**:
- v1.5: 基础版
- v2.0: 进阶版
- v3.0: 高级版
- v3.5: 最新版（推荐）

**Python示例**:
```python
import websocket
import json
import base64
import hmac
import hashlib
from datetime import datetime
from urllib.parse import urlencode, urlparse

def get_spark_auth_url(api_key, api_secret):
    """生成星火大模型鉴权URL"""
    host = "spark-api.xf-yun.com"
    path = "/v3.5/chat"
    now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature_origin = f"host: {host}\ndate: {now}\nGET {path} HTTP/1.1"
    signature_sha = hmac.new(
        api_secret.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    signature = base64.b64encode(signature_sha).decode()
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()
    params = {"authorization": authorization, "date": now, "host": host}
    return f"wss://{host}{path}?{urlencode(params)}"

def chat_with_spark(question, appid, api_key, api_secret):
    """星火大模型对话"""
    auth_url = get_spark_auth_url(api_key, api_secret)
    
    ws = websocket.create_connection(auth_url)
    
    request = {
        "header": {"app_id": appid, "uid": "user_001"},
        "parameter": {"chat": {"domain": "generalv3.5", "temperature": 0.5, "max_tokens": 4096}},
        "payload": {"message": {"text": [{"role": "user", "content": question}]}}
    }
    
    ws.send(json.dumps(request))
    result = ""
    while True:
        data = ws.recv()
        resp = json.loads(data)
        if resp.get("header", {}).get("status") == 2:
            result += resp.get("payload", {}).get("choices", {}).get("text", [{}])[0].get("content", "")
            break
        result += resp.get("payload", {}).get("choices", {}).get("text", [{}])[0].get("content", "")
    
    ws.close()
    return result
```

---

## 📝 自然语言处理 API

### 1. 文本纠错

**接口地址**: `https://api.xfyun.cn/v1/service/v1/text_correction`

**功能**: 中文文本纠错

---

### 2. 情感分析

**接口地址**: `https://api.xfyun.cn/v1/service/v1/sentiment`

**功能**: 分析文本情感倾向

---

### 3. 关键词提取

**接口地址**: `https://api.xfyun.cn/v1/service/v1/keyword`

**功能**: 提取文本关键词

---

### 4. 文本分类

**接口地址**: `https://api.xfyun.cn/v1/service/v1/text_classification`

**功能**: 文本内容分类

---

## 🔐 鉴权说明

讯飞API采用 HMAC-SHA256 签名鉴权：

```python
import base64
import hmac
import hashlib
from datetime import datetime

def generate_signature(api_key, api_secret, host, path, method="GET"):
    """生成鉴权签名"""
    now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature_origin = f"host: {host}\ndate: {now}\n{method} {path} HTTP/1.1"
    signature_sha = hmac.new(
        api_secret.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    signature = base64.b64encode(signature_sha).decode()
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode()
    return authorization, now
```

---

## 💰 免费额度

| API | 免费额度 |
|-----|---------|
| 语音合成 | 500万字符/年 |
| 语音听写 | 500万次/年 |
| 通用OCR | 500次/天 |
| 星火大模型 | 200万tokens/年 |

---

## 📚 官方文档

- 讯飞开放平台: https://www.xfyun.cn/
- API文档: https://www.xfyun.cn/doc/
- SDK下载: https://www.xfyun.cn/sdk/
- 控制台: https://console.xfyun.cn/

---

## 🔧 快速测试脚本

```python
# test_xfyun.py
import requests
import json

def test_tts():
    """测试语音合成"""
    print("测试语音合成API...")
    # 实现代码

def test_asr():
    """测试语音识别"""
    print("测试语音识别API...")
    # 实现代码

def test_ocr():
    """测试OCR"""
    print("测试OCR API...")
    # 实现代码

def test_spark():
    """测试星火大模型"""
    print("测试星火大模型API...")
    # 实现代码

if __name__ == "__main__":
    test_tts()
    test_asr()
    test_ocr()
    test_spark()
```

---

**整理人**: 小龙虾智能体
**更新时间**: 2026-04-30
