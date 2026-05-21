#!/usr/bin/env python3
"""
腾讯云 API 3.0 签名生成演示
展示完整的签名生成流程
"""

import hashlib
import hmac
import time
import os
from datetime import datetime, timezone

def generate_signature(secret_id, secret_key, service, action, payload="{}"):
    """
    生成腾讯云 API 3.0 签名
    
    Args:
        secret_id: 腾讯云 SecretId
        secret_key: 腾讯云 SecretKey
        service: 服务名称（如 cvm, hunyuan）
        action: API 动作（如 DescribeRegions）
        payload: 请求体（JSON 字符串）
    
    Returns:
        签名信息和 curl 命令
    """
    
    print("=" * 60)
    print("🦞 腾讯云 API 3.0 签名生成流程")
    print("=" * 60)
    
    # 步骤 1: 准备请求数据
    print("\n【步骤 1】请求数据")
    print(f"服务: {service}")
    print(f"动作: {action}")
    print(f"请求体: {payload}")
    
    # 时间戳
    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d')
    
    print(f"时间戳: {timestamp}")
    print(f"日期: {date}")
    
    # 步骤 2: 拼接规范请求串
    print("\n【步骤 2】拼接规范请求串")
    
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    
    canonical_headers = f"content-type:application/json\nhost:{service}.tencentcloudapi.com\nx-tc-action:{action.lower()}\n"
    signed_headers = "content-type;host;x-tc-action"
    
    # 请求体哈希
    payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    print(f"HTTP 方法: {http_request_method}")
    print(f"URI: {canonical_uri}")
    print(f"查询字符串: {canonical_querystring}")
    print(f"规范头部:\n{canonical_headers}")
    print(f"签名头部: {signed_headers}")
    print(f"请求体哈希: {payload_hash}")
    
    canonical_request = f"{http_request_method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    
    print(f"\n规范请求串:\n{canonical_request}")
    
    # 步骤 3: 拼接待签名字符串
    print("\n【步骤 3】拼接待签名字符串")
    
    algorithm = "TC3-HMAC-SHA256"
    credential_scope = f"{date}/{service}/tc3_request"
    
    canonical_request_hash = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    
    string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{canonical_request_hash}"
    
    print(f"签名算法: {algorithm}")
    print(f"时间戳: {timestamp}")
    print(f"凭证范围: {credential_scope}")
    print(f"规范请求串哈希: {canonical_request_hash}")
    print(f"\n待签名字符串:\n{string_to_sign}")
    
    # 步骤 4: 计算签名
    print("\n【步骤 4】计算签名")
    
    # 派生密钥
    secret_date = hmac.new(
        f"TC3{secret_key}".encode('utf-8'),
        date.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    secret_service = hmac.new(
        secret_date,
        service.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    secret_signing = hmac.new(
        secret_service,
        "tc3_request".encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    # 计算签名
    signature = hmac.new(
        secret_signing,
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    print(f"签名: {signature}")
    
    # 步骤 5: 拼接 Authorization
    print("\n【步骤 5】拼接 Authorization")
    
    authorization = f"{algorithm} Credential={secret_id}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    
    print(f"Authorization: {authorization}")
    
    # 生成 curl 命令
    curl = f'''curl -X POST 'https://{service}.tencentcloudapi.com/' \\
  -H 'Content-Type: application/json' \\
  -H 'Host: {service}.tencentcloudapi.com' \\
  -H 'X-TC-Action: {action}' \\
  -H 'X-TC-Version: 2017-03-12' \\
  -H 'X-TC-Timestamp: {timestamp}' \\
  -H 'X-TC-Language: zh-CN' \\
  -H 'Authorization: {authorization}' \\
  -d '{payload}' '''
    
    print("\n【curl 命令】")
    print(curl)
    
    print("\n" + "=" * 60)
    print("✅ 签名生成完成")
    print("=" * 60)
    
    return {
        "timestamp": timestamp,
        "authorization": authorization,
        "signature": signature,
        "curl": curl
    }

# 测试
if __name__ == "__main__":
    # 腾讯云密钥 - 请从环境变量读取
    import os
    SECRET_ID = os.environ.get("TENCENT_SECRET_ID", "[REDACTED]")
    SECRET_KEY = os.environ.get("TENCENT_SECRET_KEY", "[REDACTED]")
    
    # 测试 1: DescribeRegions
    print("\n\n")
    result1 = generate_signature(SECRET_ID, SECRET_KEY, "cvm", "DescribeRegions")
    
    # 测试 2: ChatCompletions
    print("\n\n")
    result2 = generate_signature(
        SECRET_ID, 
        SECRET_KEY, 
        "hunyuan", 
        "ChatCompletions", 
        '{"Model":"hunyuan-lite","Messages":[{"Role":"user","Content":"你好"}]}'
    )
