# 讯飞星火平台 API 配置

**平台**: 腾讯星辰 (讯飞星火)  
**区域**: 华北 1 (北京)  
**最后更新**: 2026-05-07 03:19 GMT+8

---

## 🔐 认证信息

```json
{
  "APPID": "fc1002ac",
  "APIKey": "1bc9c35c32ebf8c702ea62ae8db43082",
  "APISecret": "Zjg2N2M3YTg0OTFiYjY2MDliNDkyNWEx"
}
```

---

## 📡 API 端点

### 1. Hunyuan OCR (图像理解/OCR)

**模型 ID**: `xophunyuanocr`

**WebSocket 地址**:
```
wss://maas-api.cn-huabei-1.xf-yun.com/v1.1/vl
```

**HTTP 地址**:
```
https://maas-api.cn-huabei-1.xf-yun.com/v2/vl
```

**请求示例**:
```json
{
  "header": {
    "app_id": "fc1002ac",
    "uid": "user1"
  },
  "parameter": {
    "vl": {
      "domain": "xophunyuanocr",
      "threshold": 0.6,
      "max_tokens": 4096
    }
  },
  "payload": {
    "image": "data:image/jpeg;base64,<base64_encoded_image>"
  }
}
```

---

### 2. Stable Diffusion XL Base (文生图) ❌ **不可用**

**模型 ID**: `xssdxl`

**状态**: 许可证不足 (错误码：11201)

**原因**: APPID `fc1002ac` 没有 xssdxl 模型的访问权限

**解决方案**: 需要在讯飞控制台激活或购买许可证

**接口地址**:
```
https://maas-api.cn-huabei-1.xf-yun.com/v2.1/tti
```

> ⚠️ 此模型暂时不可用，请等待激活后再使用

**请求示例**:
```json
{
  "header": {
    "app_id": "12345",
    "uid": "12345"
  },
  "parameter": {
    "chat": {
      "domain": "xssdxl",
      "width": 1024,
      "height": 1024,
      "seed": 42,
      "num_inference_steps": 20,
      "guidance_scale": 5.0,
      "scheduler": "Euler"
    }
  },
  "payload": {
    "message": {
      "text": [
        {"role": "user", "content": "A beautiful mountain landscape"}
      ]
    },
    "negative_prompts": {
      "text": "blurry, low quality"
    }
  }
}
```

**支持的分辨率**:
- 768x768
- 1024x1024
- 576x1024
- 768x1024
- 1024x576
- 1024x768

**支持的调度器**:
- DPM++ 2M Karras
- DPM++ SDE Karras
- DDIM
- Euler a
- Euler

---

### 3. Qwen-Image-2512 (文生图) ❌ **不可用**

**模型 ID**: `xopqwentti20b`

**状态**: 需要进一步测试

**接口地址**:
```
https://maas-api.cn-huabei-1.xf-yun.com/v2.1/tti
```

> ℹ️ 此模型可用性待确认

**请求示例**: 同 Stable Diffusion XL Base

---

## 🔧 Python 使用示例

### Hunyuan OCR 示例

```python
import base64
import json
import hmac
import hashlib
from datetime import datetime, timezone
from urllib.request import Request, urlopen

# 配置
API_KEY = "1bc9c35c32ebf8c702ea62ae8db43082"
API_SECRET = "Zjg2N2M3YTg0OTFiYjY2MDliNDkyNWEx"
APP_ID = "fc1002ac"
HOST = "maas-api.cn-huabei-1.xf-yun.com"
API_PATH = "/v2/vl"

# 读取图片
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# 构建签名
date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
sign_str = f"host: {HOST}\ndate: {date}\nPOST {API_PATH} HTTP/1.1"
signature = base64.b64encode(
    hmac.new(API_SECRET.encode(), sign_str.encode(), hashlib.sha256).digest()
).decode()

authorization = f'api_key="{API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'

# 请求
data = {
    "header": {"app_id": APP_ID, "uid": "user1"},
    "parameter": {"vl": {"domain": "xophunyuanocr", "max_tokens": 4096}},
    "payload": {"image": f"data:image/jpeg;base64,{image_data}"}
}

req = Request(
    f"https://{HOST}{API_PATH}",
    data=json.dumps(data).encode(),
    headers={
        "Authorization": authorization,
        "Content-Type": "application/json",
        "Host": HOST,
        "Date": date
    },
    method="POST"
)

with urlopen(req) as response:
    result = json.loads(response.read().decode())
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## 📝 注意事项

1. **鉴权**: 必须使用 HMAC-SHA256 签名
2. **图片格式**: 支持 JPEG, PNG 等常见格式
3. **图片大小**: 建议不超过 10MB
4. **超时**: 图片分析可能需要较长时间，建议设置 60 秒超时
5. **错误处理**: 注意检查返回的 error code

---

## 🔗 相关文档

- [讯飞星火开放平台](https://www.xfyun.cn/doc/spark/online_api.html)
- [星辰平台控制台](https://console.xfyun.cn/services/tti)

---

**⚠️ 安全提醒**: 
- 不要将 API Key 提交到公开代码库
- 定期轮换密钥
- 限制 API 访问权限
