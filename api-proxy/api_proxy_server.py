"""
统一LLM API代理服务
封装多个免费AI平台，提供统一调用接口
"""

from flask import Flask, request, jsonify
from openai import OpenAI
import logging
from datetime import datetime
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/.openclaw/workspace/api-proxy/logs/proxy.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# API配置
API_CONFIG = {
    "github": {
        "base_url": "https://models.inference.ai.azure.com",
        "api_key": "[GITHUB_TOKEN]",
        "models": ["gpt-4o-mini", "gpt-4o", "DeepSeek-V3-0324", "Llama-4-Scout-17B-16E-Instruct"],
        "default_model": "gpt-4o-mini"
    }
}

class UnifiedAPIProxy:
    """统一API代理"""
    
    def __init__(self):
        self.clients = {}
        self._init_clients()
    
    def _init_clients(self):
        """初始化所有客户端"""
        for provider, config in API_CONFIG.items():
            try:
                self.clients[provider] = OpenAI(
                    base_url=config["base_url"],
                    api_key=config["api_key"]
                )
                logger.info(f"初始化 {provider} 客户端成功")
            except Exception as e:
                logger.error(f"初始化 {provider} 客户端失败: {e}")
    
    def call(self, provider, prompt, model=None, temperature=0.7, max_tokens=1000):
        """统一调用接口"""
        try:
            if provider not in self.clients:
                return {"success": False, "error": f"不支持的provider: {provider}"}
            
            config = API_CONFIG[provider]
            client = self.clients[provider]
            
            # 使用默认模型
            if not model:
                model = config["default_model"]
            
            # 验证模型
            if model not in config["models"]:
                logger.warning(f"模型 {model} 不在推荐列表中，可能不可用")
            
            logger.info(f"调用 {provider} - {model}")
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = {
                "success": True,
                "provider": provider,
                "model": model,
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"调用成功: {provider} - {model}")
            return result
            
        except Exception as e:
            logger.error(f"调用失败: {provider} - {model} - {str(e)}")
            return {
                "success": False,
                "provider": provider,
                "model": model,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def list_providers(self):
        """列出所有可用的provider"""
        return {
            "providers": list(API_CONFIG.keys()),
            "details": {
                provider: {
                    "models": config["models"],
                    "default_model": config["default_model"]
                }
                for provider, config in API_CONFIG.items()
            }
        }

# 初始化代理
proxy = UnifiedAPIProxy()

@app.route('/', methods=['GET'])
def index():
    """首页"""
    return jsonify({
        "service": "统一LLM API代理服务",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "/api/chat": "POST - 调用AI模型",
            "/api/providers": "GET - 查看可用provider",
            "/health": "GET - 健康检查"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/providers', methods=['GET'])
def list_providers():
    """列出所有可用的provider"""
    return jsonify(proxy.list_providers())

@app.route('/api/chat', methods=['POST'])
def chat():
    """统一聊天接口"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"success": False, "error": "请求体不能为空"}), 400
        
        provider = data.get('provider', 'github')
        prompt = data.get('prompt')
        model = data.get('model')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        if not prompt:
            return jsonify({"success": False, "error": "prompt不能为空"}), 400
        
        result = proxy.call(provider, prompt, model, temperature, max_tokens)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"处理请求失败: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/chat/batch', methods=['POST'])
def batch_chat():
    """批量调用接口"""
    try:
        data = request.json
        prompts = data.get('prompts', [])
        provider = data.get('provider', 'github')
        model = data.get('model')
        
        if not prompts:
            return jsonify({"success": False, "error": "prompts不能为空"}), 400
        
        results = []
        for prompt in prompts:
            result = proxy.call(provider, prompt, model)
            results.append(result)
        
        return jsonify({
            "success": True,
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        logger.error(f"批量处理失败: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    logger.info("启动统一LLM API代理服务...")
    logger.info(f"可用provider: {list(API_CONFIG.keys())}")
    app.run(host='0.0.0.0', port=5000, debug=False)
