# 带超算中心API管理文档

> 创建时间: 2026-05-02
> 状态: ✅ 已配置并测试成功

---

## 一、API密钥

- **API Key**: `sk-NjQzLTExMzE0OTg1MTExLTE3NzUxNDMyMDg2MzM=`
- **鉴权方式**: Bearer Token
- **状态**: ✅ 已配置

---

## 二、Chat API（20个模型可用）

### 基本信息
- **接口**: `https://api.scnet.cn/api/llm/v1/chat/completions`
- **方法**: POST
- **Content-Type**: application/json

### 可用模型
| 模型 | 类型 | 状态 |
|------|------|------|
| DeepSeek-V3.2 | 通用对话 | ✅ 已测试 |
| DeepSeek-V4-Pro | 通用对话 | ✅ 已测试 |
| DeepSeek-V4-Flash | 快速对话 | ✅ 可用 |
| DeepSeek-R1-0528 | 推理模型 | ✅ 可用 |
| Qwen3.6-Max | 通用对话 | ✅ 已测试 |
| Qwen3.6-Plus | 通用对话 | ✅ 可用 |
| Qwen3.6-Flash | 快速对话 | ✅ 可用 |
| Qwen3-235B-A22B | 大模型 | ✅ 可用 |
| Qwen3-30B-A3B | 中型模型 | ✅ 可用 |
| QwQ-32B | 推理模型 | ✅ 可用 |
| GLM-5.1 | 通用对话 | ✅ 已测试 |
| Kimi-K2.6 | 通用对话 | ✅ 已测试 |
| MiniMax-M2.5 | 通用对话 | ✅ 可用 |

### 调用示例

**cURL**:
```bash
curl 'https://api.scnet.cn/api/llm/v1/chat/completions' \
--header 'Authorization: Bearer sk-NjQzLTExMzE0OTg1MTExLTE3NzUxNDMyMDg2MzM=' \
--header 'Content-Type: application/json' \
--data '{
  "model": "DeepSeek-V3.2",
  "messages": [{"role": "user", "content": "你好"}],
  "max_tokens": 100
}'
```

**Python**:
```python
import requests

url = "https://api.scnet.cn/api/llm/v1/chat/completions"
headers = {
    "Authorization": "Bearer sk-NjQzLTExMzE0OTg1MTExLTE3NzUxNDMyMDg2MzM=",
    "Content-Type": "application/json"
}
data = {
    "model": "DeepSeek-V3.2",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 100
}
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

---

## 三、OCR API

### 基本信息
- **接口**: `https://api.scnet.cn/api/llm/v1/ocr/recognize`
- **方法**: POST
- **Content-Type**: multipart/form-data
- **参数**: `ocrType=general`

### 调用示例

**cURL**:
```bash
curl 'https://api.scnet.cn/api/llm/v1/ocr/recognize' \
--header 'Authorization: Bearer sk-NjQzLTExMzE0OTg1MTExLTE3NzUxNDMyMDg2MzM=' \
--form 'file=@image.jpg' \
--form 'ocrType=general'
```

**Python**:
```python
import requests

url = "https://api.scnet.cn/api/llm/v1/ocr/recognize"
headers = {"Authorization": "Bearer sk-NjQzLTExMzE0OTg1MTExLTE3NzUxNDMyMDg2MzM="}
files = {"file": open("image.jpg", "rb")}
data = {"ocrType": "general"}
response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

---

## 四、文生视频 API

### 基本信息
- **接口**: `https://web-2039627502965784578-higa.dzai.scnet.cn:58043/gradio_api/call/generate_video`
- **模型**: Wan2.2-TI2V-5B
- **Web界面**: https://web-2039627502965784578-higa.dzai.scnet.cn:58043/

### 参数说明
| 参数 | 说明 | 默认值 | 范围 |
|------|------|--------|------|
| image | 可选图片 | null | 图片文件 |
| prompt | 提示词 | - | 文本 |
| height | 输出高度 | 704 | 128-1280 |
| width | 输出宽度 | 1280 | 128-1280 |
| duration_seconds | 时长（秒） | 2.0 | 0.3-2.0 |
| sampling_steps | 采样步数 | 38 | 10-50 |
| guide_scale | 引导比例 | 5.0 | 1.0-10.0 |
| shift | 采样偏移 | 5.0 | 1.0-20.0 |
| seed | 随机种子 | -1 | 整数 |

### 调用示例

**Python**:
```python
import requests

url = "https://web-2039627502965784578-higa.dzai.scnet.cn:58043/gradio_api/call/generate_video"
payload = {
    "data": [
        None,  # image
        "一只可爱的金毛犬在公园里奔跑",  # prompt
        704,   # height
        1280,  # width
        2.0,   # duration
        38,    # steps
        5.0,   # guide_scale
        5.0,   # shift
        -1     # seed
    ]
}
response = requests.post(url, json=payload)
event_id = response.json()["event_id"]
print(f"任务ID: {event_id}")
```

---

## 五、已部署模型

### 当前状态
- **V3**: 已删除（模型太卡）
- **V1**: 传输中

### 历史部署记录
- V3 (已删除): 西南一区【四川】异构加速卡AI * 1卡
  - 模型: wan2_2_ti2v_5b, hunyuan, deepseek_ocr
  - 删除原因: 模型太卡

---

## 六、测试记录

### 2026-05-02 测试结果

| API | 状态 | 备注 |
|-----|------|------|
| Chat API | ✅ 成功 | DeepSeek-V3.2响应正常 |
| OCR API | ✅ 成功 | 识别准确 |
| 文生视频 API | ✅ 可用 | 任务提交成功，长连接不稳定 |

---

## 七、注意事项

1. **文生视频API**: 长连接等待结果不稳定，建议通过Web界面操作
2. **OCR API**: 只支持 `ocrType=general` 参数
3. **Chat API**: 20个模型可用，推荐使用 DeepSeek-V3.2 或 Qwen3.6-Max

---

> 🌌 **星辰大脑**
> "带超算中心API管理文档，持续更新中"
