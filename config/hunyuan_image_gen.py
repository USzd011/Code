#!/usr/bin/env python3
"""
腾讯混元文生图完整工具
支持 TextToImageLite 和 TextToImagePro
"""

import subprocess
import json
import base64
import os
from datetime import datetime
from typing import Dict, Optional

class HunyuanImageGen:
    """腾讯混元文生图客户端"""
    
    def __init__(self):
        self.service = "aiart"
        self.version = "2022-12-29"
        self.region = "ap-guangzhou"
    
    def text_to_image_lite(
        self,
        prompt: str,
        negative_prompt: str = "",
        resolution: str = "1024:1024",
        seed: Optional[int] = None,
        logo_add: int = 0,
        rsp_img_type: str = "base64"
    ) -> Dict:
        """
        混元文生图 Lite 版本
        
        Args:
            prompt: 文本描述（最多1024个utf-8字符）
            negative_prompt: 反向提示词（最多1024个utf-8字符）
            resolution: 生成图分辨率，默认1024:1024
                支持比例: 1:1, 3:4, 4:3, 9:16, 16:9
                支持长边: 160-4096px
            seed: 随机种子（0或空=随机，正数=固定）
            logo_add: 添加标识（1=添加，0=不添加）
            rsp_img_type: 返回方式（base64 或 url）
        
        Returns:
            生成结果
        """
        # 构建参数
        params = {
            "Prompt": prompt,
            "Resolution": resolution,
            "LogoAdd": logo_add,
            "RspImgType": rsp_img_type
        }
        
        if negative_prompt:
            params["NegativePrompt"] = negative_prompt
        
        if seed is not None:
            params["Seed"] = seed
        
        # 调用 API
        cmd = [
            "tccli", "aiart", "TextToImageLite",
            "--Region", self.region,
            "--output", "json"
        ]
        
        # 添加参数
        for key, value in params.items():
            cmd.extend([f"--{key}", str(value)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                
                # 保存图像
                if rsp_img_type == "base64" and "ResultImage" in response:
                    img_data = response["ResultImage"]
                    img_bytes = base64.b64decode(img_data)
                    
                    # 生成文件名
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"hunyuan_lite_{timestamp}.png"
                    
                    # 保存文件
                    with open(filename, "wb") as f:
                        f.write(img_bytes)
                    
                    response["saved_file"] = filename
                    response["file_size"] = len(img_bytes)
                
                return {
                    "success": True,
                    "data": response
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def text_to_image_pro(
        self,
        prompt: str,
        negative_prompt: str = "",
        resolution: str = "1024:1024",
        style: str = "写实",
        seed: Optional[int] = None,
        logo_add: int = 0,
        rsp_img_type: str = "base64"
    ) -> Dict:
        """
        混元文生图 Pro 版本（提交任务）
        
        Args:
            prompt: 文本描述
            negative_prompt: 反向提示词
            resolution: 生成图分辨率
            style: 风格（写实/动漫/油画/水彩等）
            seed: 随机种子
            logo_add: 添加标识
            rsp_img_type: 返回方式
        
        Returns:
            任务ID
        """
        # 构建参数
        params = {
            "Prompt": prompt,
            "Resolution": resolution,
            "Style": style,
            "LogoAdd": logo_add,
            "RspImgType": rsp_img_type
        }
        
        if negative_prompt:
            params["NegativePrompt"] = negative_prompt
        
        if seed is not None:
            params["Seed"] = seed
        
        # 调用 API
        cmd = [
            "tccli", "aiart", "SubmitTextToImageProJob",
            "--Region", self.region,
            "--output", "json"
        ]
        
        # 添加参数
        for key, value in params.items():
            cmd.extend([f"--{key}", str(value)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                
                return {
                    "success": True,
                    "task_id": response.get("JobId"),
                    "data": response
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def query_pro_job(self, job_id: str) -> Dict:
        """
        查询 Pro 任务状态
        
        Args:
            job_id: 任务ID
        
        Returns:
            任务状态和结果
        """
        cmd = [
            "tccli", "aiart", "QueryTextToImageProJob",
            "--Region", self.region,
            "--JobId", job_id,
            "--output", "json"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                
                return {
                    "success": True,
                    "status": response.get("JobStatus"),
                    "data": response
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_anime(self, description: str) -> Dict:
        """生成动漫风格图像"""
        return self.text_to_image_lite(
            prompt=f"动漫风格，{description}，精美细节，高质量",
            resolution="1024:1024"
        )
    
    def generate_realistic(self, description: str) -> Dict:
        """生成写实风格图像"""
        return self.text_to_image_lite(
            prompt=f"写实风格，{description}，超高清，细节丰富",
            resolution="1024:1024"
        )
    
    def generate_portrait(self, description: str) -> Dict:
        """生成人物肖像"""
        return self.text_to_image_lite(
            prompt=f"高质量人物肖像，{description}，精细面部细节，专业摄影",
            resolution="1024:1024"
        )
    
    def generate_landscape(self, description: str) -> Dict:
        """生成风景"""
        return self.text_to_image_lite(
            prompt=f"壮丽风景，{description}，超高清，细节丰富",
            resolution="1920:1080"
        )

# 测试
if __name__ == "__main__":
    print("=" * 60)
    print("🦞 腾讯混元文生图测试")
    print("=" * 60)
    
    # 创建客户端
    img_gen = HunyuanImageGen()
    
    # 测试 1: Lite 版本
    print("\n【测试 1】TextToImageLite - 动漫风格")
    result = img_gen.generate_anime("一只可爱的橘猫，坐在阳光明媚的窗台上")
    
    if result["success"]:
        print("✅ 生成成功")
        if "saved_file" in result["data"]:
            print(f"文件: {result['data']['saved_file']}")
            print(f"大小: {result['data']['file_size']} bytes")
        print(f"种子: {result['data'].get('Seed')}")
    else:
        print(f"❌ 生成失败: {result['error']}")
    
    # 测试 2: 写实风格
    print("\n【测试 2】TextToImageLite - 写实风格")
    result = img_gen.generate_realistic("一座古老的城堡，坐落在山顶，夕阳西下")
    
    if result["success"]:
        print("✅ 生成成功")
        if "saved_file" in result["data"]:
            print(f"文件: {result['data']['saved_file']}")
            print(f"大小: {result['data']['file_size']} bytes")
    else:
        print(f"❌ 生成失败: {result['error']}")
    
    print("\n" + "=" * 60)
    print("✅ 混元文生图测试完成")
    print("=" * 60)
