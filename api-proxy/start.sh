#!/bin/bash
# API代理服务启动脚本

echo "==================================="
echo "统一LLM API代理服务"
echo "==================================="

# 检查依赖
echo "检查依赖..."
pip install flask openai -q

# 启动服务
echo "启动服务..."
cd /root/.openclaw/workspace/api-proxy
python api_proxy_server.py
