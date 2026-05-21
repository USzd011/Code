# API代理服务使用文档

## 🚀 快速启动

### 启动服务
```bash
cd /root/.openclaw/workspace/api-proxy
chmod +x start.sh
./start.sh
```

### 后台启动
```bash
nohup python api_proxy_server.py > logs/server.log 2>&1 &
```

---

## 📡 API接口

### 1. 首页
```bash
curl http://localhost:5000/
```

### 2. 查看可用provider
```bash
curl http://localhost:5000/api/providers
```

### 3. 调用AI模型
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "github",
    "prompt": "你好，请介绍一下自己",
    "model": "gpt-4o-mini"
  }'
```

### 4. 批量调用
```bash
curl -X POST http://localhost:5000/api/chat/batch \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "github",
    "model": "gpt-4o-mini",
    "prompts": ["你好", "介绍一下自己", "写一段代码"]
  }'
```

---

## 🐍 Python调用示例

```python
import requests

# API地址
API_URL = "http://localhost:5000/api/chat"

# 调用函数
def call_ai(prompt, model="gpt-4o-mini", provider="github"):
    response = requests.post(API_URL, json={
        "provider": provider,
        "prompt": prompt,
        "model": model
    })
    return response.json()

# 使用示例
result = call_ai("你好，请写一段Python快速排序代码")
print(result["content"])
```

---

## 📊 可用模型

### GitHub Models
- gpt-4o-mini（默认）
- gpt-4o
- DeepSeek-V3-0324
- Llama-4-Scout-17B-16E-Instruct

---

## 🔧 配置

### 添加新的provider

编辑 `api_proxy_server.py`，在 `API_CONFIG` 中添加：

```python
API_CONFIG = {
    "github": {...},
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "你的API_KEY",
        "models": ["google/gemma-3-1b-it:free"],
        "default_model": "google/gemma-3-1b-it:free"
    }
}
```

---

## 📝 日志

日志文件位置：
- `/root/.openclaw/workspace/api-proxy/logs/proxy.log`

查看日志：
```bash
tail -f logs/proxy.log
```

---

## ⚠️ 注意事项

1. 服务默认运行在 `localhost:5000`
2. 生产环境建议使用 gunicorn 部署
3. 注意各平台的频率限制
4. 不要传输敏感数据

---

## 🚀 生产部署

使用 gunicorn 部署：
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_proxy_server:app
```

使用 systemd 管理：
```bash
# 创建服务文件
sudo nano /etc/systemd/system/api-proxy.service

# 内容
[Unit]
Description=API Proxy Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/api-proxy
ExecStart=/usr/bin/python3 api_proxy_server.py
Restart=always

[Install]
WantedBy=multi-user.target

# 启动服务
sudo systemctl start api-proxy
sudo systemctl enable api-proxy
```
