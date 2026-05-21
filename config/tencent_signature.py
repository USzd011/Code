#!/usr/bin/env python3
"""
腾讯云 API 3.0 签名生成工具
"""

import hashlib
import hmac
import time
from datetime import datetime

class TencentSignature:
    """腾讯云 API 3.0 签名生成器"""
    
    def __init__(self, secret_id: str, secret_key: str):
        """
        初始化
        
        Args:
            secret_id: 腾讯云 SecretId
            secret_key: 腾讯云 SecretKey
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
    
    def sign(self, service: str, action: str, payload: str = "{}", region: str = "") -> dict:
        """
        生成签名
        
        Args:
            service: 服务名称（如 cvm, hunyuan）
            action: API 动作（如 DescribeRegions）
            payload: 请求体（JSON 字符串）
            region: 地域（可选）
        
        Returns:
            签名信息
        """
        # 时间戳
        timestamp = int(time.time())
        date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        
        # 1. 拼接规范请求串
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        
        canonical_headers = f"content-type:application/json\nhost:{service}.tencentcloudapi.com\nx-tc-action:{action.lower()}\n"
        signed_headers = "content-type;host;x-tc-action"
        
        # 请求体哈希
        payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
        canonical_request = f"{http_request_method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
        
        # 2. 拼接待签名字符串
        algorithm = "TC3-HMAC-SHA256"
        credential_scope = f"{date}/{service}/tc3_request"
        
        canonical_request_hash = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        
        string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{canonical_request_hash}"
        
        # 3. 计算签名
        secret_date = hmac.new(
            f"TC3{self.secret_key}".encode('utf-8'),
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
        
        signature = hmac.new(
            secret_signing,
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # 4. 拼接 Authorization
        authorization = f"{algorithm} Credential={self.secret_id}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
        
        return {
            "timestamp": timestamp,
            "authorization": authorization,
            "service": service,
            "action": action,
            "host": f"{service}.tencentcloudapi.com",
            "payload": payload
        }
    
    def generate_curl(self, service: str, action: str, payload: str = "{}", region: str = "") -> str:
        """
        生成 curl 命令
        
        Args:
            service: 服务名称
            action: API 动作
            payload: 请求体
            region: 地域
        
        Returns:
            curl 命令
        """
        sign_info = self.sign(service, action, payload, region)
        
        curl = f'''curl -X POST 'https://{sign_info["host"]}/' \\
  -H 'Content-Type: application/json' \\
  -H 'Host: {sign_info["host"]}' \\
  -H 'X-TC-Action: {action}' \\
  -H 'X-TC-Version: 2017-03-12' \\
  -H 'X-TC-Timestamp: {sign_info["timestamp"]}' \\
  -H 'X-TC-Language: zh-CN' \\
  -H 'Authorization: {sign_info["authorization"]}' \\
  -d '{payload}' '''
        
        return curl

# 测试
if __name__ == "__main__":
    # 腾讯云密钥
    SECRET_ID = "[TENCENT_SECRET_ID]"
    SECRET_KEY = "[TENCENT_SECRET_KEY]"
    
    # 创建签名器
    signer = TencentSignature(SECRET_ID, SECRET_KEY)
    
    # 生成签名
    print("=" * 60)
    print("🦞 腾讯云 API 3.0 签名生成测试")
    print("=" * 60)
    
    # 测试 1: DescribeRegions
    print("\n【测试 1】DescribeRegions")
    curl = signer.generate_curl("cvm", "DescribeRegions")
    print(curl)
    
    # 测试 2: ChatCompletions
    print("\n【测试 2】ChatCompletions")
    payload = '{"Model":"hunyuan-lite","Messages":[{"Role":"user","Content":"你好"}]}'
    curl = signer.generate_curl("hunyuan", "ChatCompletions", payload)
    print(curl)
    
    print("\n" + "=" * 60)
    print("✅ 签名生成测试完成")
    print("=" * 60)
