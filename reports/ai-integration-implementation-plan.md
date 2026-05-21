# AI工具集成实施方案

> 生成时间: 2026-05-05
> 目标: 为杨欢设计可落地的AI工具集成方案

---

## 一、现状分析

### 已有资源 (来自TOOLS.md)

| 资源 | 状态 | 可用性 |
|-----|------|--------|
| Google Gemini API | ✅ 已配置 | 免费额度充足 |
| GitHub Models | ✅ 已配置 | 多模型免费 |
| 讯飞星火RPA | ✅ 已配置 | 中文语音交互 |
| 扣子平台 | ✅ 已配置 | Agent编排 |
| 百度OCR | ✅ 已配置 | 文字识别 |

### 待补充资源

| 资源 | 优先级 | 获取难度 | 预估成本 |
|-----|--------|---------|---------|
| OpenAI API | 高 | 低 | $20-50/月 |
| Anthropic API | 高 | 低 | $20-50/月 |
| DeepSeek API | 中 | 低 | $10-20/月 |
| ElevenLabs API | 低 | 低 | $5-20/月 |

---

## 二、集成架构设计

### 2.1 总体架构

```
┌────────────────────────────────────────────────────────────────┐
│                      OpenClaw Agent System                      │
│                        (小龙虾运行平台)                          │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                    AI Gateway Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  路由决策   │  │  成本控制   │  │  降级策略   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  缓存管理   │  │  日志监控   │  │  限流熔断   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   LLM Pool   │      │  Image Pool  │      │  Audio Pool  │
│              │      │              │      │              │
│ • Gemini     │      │ • DALL-E     │      │ • Whisper    │
│ • GPT-4o     │      │ • SD (本地)  │      │ • ElevenLabs │
│ • Claude     │      │ • Flux       │      │ • 讯飞语音   │
│ • DeepSeek   │      │              │      │              │
│ • GitHub     │      │              │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
```

### 2.2 路由决策逻辑

```python
# 路由决策树
class AIRouter:
    def route(self, task_type: str, complexity: str, budget: str) -> str:
        """
        根据任务类型、复杂度、预算选择最优模型
        """
        
        # 任务类型映射
        task_model_map = {
            "code": ["claude-3-5-sonnet", "deepseek-v3"],
            "writing": ["gemini-2-0-flash", "gpt-4o"],
            "analysis": ["claude-3-5-sonnet", "gpt-4o"],
            "chat": ["gemini-2-0-flash", "deepseek-chat"],
            "image": ["dall-e-3", "stable-diffusion"],
            "audio_transcribe": ["whisper-1"],
            "audio_synthesize": ["elevenlabs"]
        }
        
        # 复杂度调整
        if complexity == "high":
            # 升级到更强模型
            return self._upgrade_model(task_model_map[task_type][0])
        elif complexity == "low":
            # 使用经济模型
            return self._economize_model(task_model_map[task_type][0])
        
        # 预算限制
        if budget == "free":
            return self._free_fallback(task_type)
        
        return task_model_map[task_type][0]
    
    def _upgrade_model(self, model: str) -> str:
        upgrades = {
            "gemini-2-0-flash": "gemini-1-5-pro",
            "deepseek-chat": "claude-3-5-sonnet",
            "gpt-4o-mini": "gpt-4o"
        }
        return upgrades.get(model, model)
    
    def _economize_model(self, model: str) -> str:
        economizes = {
            "claude-3-5-sonnet": "claude-3-5-haiku",
            "gpt-4o": "gpt-4o-mini",
            "gemini-1-5-pro": "gemini-2-0-flash"
        }
        return economizes.get(model, model)
    
    def _free_fallback(self, task_type: str) -> str:
        free_models = {
            "chat": "gemini-2-0-flash",
            "code": "github:deepseek-v3",
            "writing": "gemini-2-0-flash",
            "analysis": "github:gpt-4o"
        }
        return free_models.get(task_type, "gemini-2-0-flash")
```

---

## 三、分阶段实施计划

### Phase 1: 基础集成 (Week 1)

**目标**: 建立基础AI调用能力

**任务清单**
- [x] Gemini API 已配置
- [x] GitHub Models 已配置
- [ ] 创建统一API封装层
- [ ] 实现基础路由逻辑
- [ ] 添加错误处理和重试机制

**代码实现**
```python
# ~/.openclaw/workspace/lib/ai_gateway.py

from typing import Optional, Dict, Any, List
import os
import time
import logging
from dataclasses import dataclass

@dataclass
class AIConfig:
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None

class AIGateway:
    """统一AI调用网关"""
    
    def __init__(self):
        self.configs = self._load_configs()
        self.logger = logging.getLogger("ai_gateway")
        
    def _load_configs(self) -> Dict[str, AIConfig]:
        """加载API配置"""
        return {
            "gemini": AIConfig(
                provider="gemini",
                model="gemini-2.0-flash",
                api_key=os.getenv("GOOGLE_API_KEY", "[GEMINI_API_KEY]")
            ),
            "github": AIConfig(
                provider="github",
                model="gpt-4o",
                api_key=os.getenv("GITHUB_TOKEN", "[GITHUB_TOKEN]"),
                base_url="https://models.inference.ai.azure.com"
            ),
            "deepseek": AIConfig(
                provider="deepseek",
                model="deepseek-chat",
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com/v1"
            )
        }
    
    def chat(
        self,
        message: str,
        provider: str = "gemini",
        model: Optional[str] = None,
        system: Optional[str] = None,
        max_retries: int = 3,
        fallback_providers: List[str] = ["gemini", "github"]
    ) -> str:
        """统一对话接口"""
        
        for attempt in range(max_retries):
            for prov in fallback_providers:
                try:
                    return self._call_provider(prov, message, model, system)
                except Exception as e:
                    self.logger.warning(f"Provider {prov} failed: {e}")
                    time.sleep(2 ** attempt)
        
        raise Exception("All providers failed")
    
    def _call_provider(
        self,
        provider: str,
        message: str,
        model: Optional[str],
        system: Optional[str]
    ) -> str:
        """调用具体Provider"""
        
        config = self.configs.get(provider)
        if not config or not config.api_key:
            raise ValueError(f"Provider {provider} not configured")
        
        model = model or config.model
        
        if provider == "gemini":
            return self._call_gemini(config.api_key, model, message, system)
        else:
            return self._call_openai_compatible(config, model, message, system)
    
    def _call_gemini(
        self,
        api_key: str,
        model: str,
        message: str,
        system: Optional[str]
    ) -> str:
        """调用Gemini API"""
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model_obj = genai.GenerativeModel(
            model,
            system_instruction=system
        )
        response = model_obj.generate_content(message)
        return response.text
    
    def _call_openai_compatible(
        self,
        config: AIConfig,
        model: str,
        message: str,
        system: Optional[str]
    ) -> str:
        """调用OpenAI兼容API"""
        from openai import OpenAI
        
        client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

# 使用示例
gateway = AIGateway()

# 使用Gemini (免费)
response = gateway.chat("Hello!", provider="gemini")

# 使用GitHub Models (免费)
response = gateway.chat("Write code", provider="github", model="deepseek-v3")

# 自动降级
response = gateway.chat(
    "Complex analysis",
    fallback_providers=["github", "gemini"]
)
```

### Phase 2: 成本优化 (Week 2)

**目标**: 实现成本控制和缓存机制

**任务清单**
- [ ] 实现Token计数器
- [ ] 添加预算监控
- [ ] 实现语义缓存
- [ ] 添加请求限流

**代码实现**
```python
# ~/.openclaw/workspace/lib/cost_controller.py

import time
from collections import defaultdict
from typing import Dict, Optional
import hashlib

class CostController:
    """成本控制器"""
    
    def __init__(self, daily_budget: float = 10.0):
        self.daily_budget = daily_budget
        self.usage = defaultdict(float)
        self.cache: Dict[str, str] = {}
        self.request_count = defaultdict(int)
        self.rate_limits = {
            "gemini": 1500,  # RPD
            "github": 5000,
            "deepseek": 1000
        }
    
    def check_budget(self, provider: str, estimated_cost: float) -> bool:
        """检查预算"""
        total = sum(self.usage.values())
        if total + estimated_cost > self.daily_budget:
            return False
        return True
    
    def record_usage(self, provider: str, tokens_in: int, tokens_out: int):
        """记录使用量"""
        # 定价表 (每百万Token)
        pricing = {
            "gemini": {"in": 0.1, "out": 0.4},
            "github": {"in": 0, "out": 0},  # 免费
            "deepseek": {"in": 0.14, "out": 0.28},
            "openai": {"in": 2.5, "out": 10},
            "anthropic": {"in": 3, "out": 15}
        }
        
        if provider in pricing:
            cost = (
                tokens_in * pricing[provider]["in"] / 1_000_000 +
                tokens_out * pricing[provider]["out"] / 1_000_000
            )
            self.usage[provider] += cost
    
    def check_rate_limit(self, provider: str) -> bool:
        """检查速率限制"""
        today = time.strftime("%Y-%m-%d")
        key = f"{provider}:{today}"
        
        if self.request_count[key] >= self.rate_limits.get(provider, 1000):
            return False
        
        self.request_count[key] += 1
        return True
    
    def get_cache(self, message: str, threshold: float = 0.95) -> Optional[str]:
        """获取缓存结果"""
        # 简化版：使用精确匹配
        cache_key = hashlib.md5(message.encode()).hexdigest()
        return self.cache.get(cache_key)
    
    def set_cache(self, message: str, response: str):
        """设置缓存"""
        cache_key = hashlib.md5(message.encode()).hexdigest()
        self.cache[cache_key] = response
    
    def get_report(self) -> Dict:
        """获取使用报告"""
        return {
            "daily_budget": self.daily_budget,
            "total_used": sum(self.usage.values()),
            "by_provider": dict(self.usage),
            "remaining": self.daily_budget - sum(self.usage.values()),
            "cache_size": len(self.cache)
        }
```

### Phase 3: 高级功能 (Week 3)

**目标**: 实现多模态和Agent功能

**任务清单**
- [ ] 添加图像生成接口
- [ ] 添加语音识别接口
- [ ] 实现多模型协作
- [ ] 添加工具调用支持

**代码实现**
```python
# ~/.openclaw/workspace/lib/multimodal_gateway.py

from typing import Optional, List, Dict, Any
from PIL import Image
import base64

class MultimodalGateway(AIGateway):
    """多模态AI网关"""
    
    def generate_image(
        self,
        prompt: str,
        provider: str = "dalle",
        size: str = "1024x1024",
        quality: str = "standard"
    ) -> str:
        """生成图像"""
        
        if provider == "dalle":
            return self._call_dalle(prompt, size, quality)
        elif provider == "stable_diffusion":
            return self._call_sd(prompt)
        else:
            raise ValueError(f"Unknown image provider: {provider}")
    
    def _call_dalle(self, prompt: str, size: str, quality: str) -> str:
        """调用DALL-E"""
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1
        )
        return response.data[0].url
    
    def transcribe_audio(
        self,
        audio_path: str,
        provider: str = "whisper"
    ) -> str:
        """语音识别"""
        
        if provider == "whisper":
            return self._call_whisper(audio_path)
        elif provider == "xunfei":
            return self._call_xunfei(audio_path)
        else:
            raise ValueError(f"Unknown audio provider: {provider}")
    
    def _call_whisper(self, audio_path: str) -> str:
        """调用Whisper"""
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        with open(audio_path, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return response.text
    
    def analyze_image(
        self,
        image_path: str,
        question: str,
        provider: str = "gemini"
    ) -> str:
        """图像理解"""
        
        if provider == "gemini":
            return self._gemini_image_analysis(image_path, question)
        elif provider == "gpt4o":
            return self._gpt4o_image_analysis(image_path, question)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def _gemini_image_analysis(self, image_path: str, question: str) -> str:
        """Gemini图像分析"""
        import google.generativeai as genai
        
        genai.configure(api_key=self.configs["gemini"].api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        image = Image.open(image_path)
        response = model.generate_content([question, image])
        return response.text
    
    def _gpt4o_image_analysis(self, image_path: str, question: str) -> str:
        """GPT-4o图像分析"""
        from openai import OpenAI
        
        # 编码图像
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }}
                ]
            }]
        )
        return response.choices[0].message.content
```

### Phase 4: Agent编排 (Week 4)

**目标**: 实现多Agent协作

**任务清单**
- [ ] 设计Agent协作框架
- [ ] 实现任务分解
- [ ] 实现结果聚合
- [ ] 添加质量评估

**代码实现**
```python
# ~/.openclaw/workspace/lib/agent_orchestrator.py

from typing import List, Dict, Any, Callable
from dataclasses import dataclass
import concurrent.futures

@dataclass
class AgentTask:
    id: str
    type: str
    input: str
    agent: str
    dependencies: List[str] = []

class AgentOrchestrator:
    """Agent编排器"""
    
    def __init__(self, gateway: AIGateway):
        self.gateway = gateway
        self.agents = {
            "coder": {"model": "claude-3-5-sonnet", "specialty": "code"},
            "writer": {"model": "gpt-4o", "specialty": "writing"},
            "analyst": {"model": "gemini-2.0-flash", "specialty": "analysis"},
            "reviewer": {"model": "claude-3-5-sonnet", "specialty": "review"}
        }
    
    def execute_parallel(
        self,
        tasks: List[AgentTask]
    ) -> Dict[str, str]:
        """并行执行多个任务"""
        
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            for task in tasks:
                agent_config = self.agents[task.agent]
                future = executor.submit(
                    self.gateway.chat,
                    task.input,
                    provider=agent_config["model"].split(":")[0],
                    model=agent_config["model"],
                    system=f"You are a {agent_config['specialty']} expert."
                )
                futures[future] = task.id
            
            for future in concurrent.futures.as_completed(futures):
                task_id = futures[future]
                results[task_id] = future.result()
        
        return results
    
    def execute_sequential(
        self,
        tasks: List[AgentTask],
        aggregate: bool = True
    ) -> str:
        """串行执行任务链"""
        
        results = {}
        for task in tasks:
            # 等待依赖完成
            context = ""
            for dep_id in task.dependencies:
                if dep_id in results:
                    context += f"\nPrevious result ({dep_id}): {results[dep_id]}"
            
            # 执行任务
            agent_config = self.agents[task.agent]
            input_with_context = task.input + context
            
            result = self.gateway.chat(
                input_with_context,
                provider=agent_config["model"].split(":")[0],
                model=agent_config["model"],
                system=f"You are a {agent_config['specialty']} expert."
            )
            
            results[task.id] = result
        
        if aggregate:
            return self._aggregate_results(results)
        return results
    
    def _aggregate_results(self, results: Dict[str, str]) -> str:
        """聚合结果"""
        summary = "# Task Results\n\n"
        for task_id, result in results.items():
            summary += f"## {task_id}\n{result}\n\n"
        return summary
    
    def review_and_refine(
        self,
        content: str,
        review_agent: str = "reviewer",
        refine_agent: str = "writer"
    ) -> str:
        """审查并优化内容"""
        
        # Step 1: 审查
        review = self.gateway.chat(
            f"Review and critique this content:\n{content}",
            provider="gemini",
            system="You are a critical reviewer. Identify issues and suggest improvements."
        )
        
        # Step 2: 优化
        refined = self.gateway.chat(
            f"Improve this content based on the review:\n\nOriginal:\n{content}\n\nReview:\n{review}",
            provider="gemini",
            system="You are a skilled writer. Improve the content."
        )
        
        return refined
```

---

## 四、配置文件模板

### 4.1 AI Gateway配置

```yaml
# ~/.openclaw/workspace/config/ai_gateway.yaml

providers:
  gemini:
    api_key: "${GOOGLE_API_KEY}"
    models:
      - gemini-2.0-flash
      - gemini-1.5-pro
    rate_limit: 1500
    pricing:
      input: 0.1
      output: 0.4
  
  github:
    api_key: "${GITHUB_TOKEN}"
    base_url: "https://models.inference.ai.azure.com"
    models:
      - gpt-4o
      - claude-3-5-sonnet-20241022
      - deepseek-v3
      - llama-4
    rate_limit: 5000
    pricing:
      input: 0
      output: 0
  
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
    base_url: "https://api.deepseek.com/v1"
    models:
      - deepseek-chat
      - deepseek-coder
    rate_limit: 1000
    pricing:
      input: 0.14
      output: 0.28

routing:
  default_provider: gemini
  fallback_chain:
    - gemini
    - github
    - deepseek
  
  task_routing:
    code:
      primary: github:deepseek-v3
      fallback: github:claude-3-5-sonnet-20241022
    writing:
      primary: gemini:gemini-2.0-flash
      fallback: github:gpt-4o
    analysis:
      primary: github:gpt-4o
      fallback: gemini:gemini-1.5-pro

budget:
  daily_limit: 10.0
  monthly_limit: 300.0
  alert_threshold: 80%

cache:
  enabled: true
  ttl: 3600
  max_size: 1000
```

### 4.2 环境变量配置

```bash
# ~/.openclaw/workspace/config/.env

# 已有配置
GOOGLE_API_KEY=[GEMINI_API_KEY]
GITHUB_TOKEN=[GITHUB_TOKEN]

# 待申请配置
OPENAI_API_KEY=sk-xxx  # 需申请
ANTHROPIC_API_KEY=sk-ant-xxx  # 需申请
DEEPSEEK_API_KEY=sk-xxx  # 需申请
ELEVENLABS_API_KEY=xxx  # 需申请
```

---

## 五、监控和日志

### 5.1 监控指标

```python
# ~/.openclaw/workspace/lib/ai_monitor.py

from typing import Dict, List
import time
import json
from collections import defaultdict

class AIMonitor:
    """AI调用监控"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.errors = defaultdict(int)
    
    def record_call(
        self,
        provider: str,
        model: str,
        latency_ms: float,
        tokens_in: int,
        tokens_out: int,
        success: bool
    ):
        """记录调用"""
        timestamp = time.time()
        
        self.metrics["calls"].append({
            "timestamp": timestamp,
            "provider": provider,
            "model": model,
            "latency_ms": latency_ms,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "success": success
        })
        
        if not success:
            self.errors[f"{provider}:{model}"] += 1
    
    def get_stats(self, period_hours: int = 24) -> Dict:
        """获取统计"""
        cutoff = time.time() - period_hours * 3600
        
        recent_calls = [
            c for c in self.metrics["calls"]
            if c["timestamp"] > cutoff
        ]
        
        if not recent_calls:
            return {"period_hours": period_hours, "calls": 0}
        
        return {
            "period_hours": period_hours,
            "total_calls": len(recent_calls),
            "success_rate": sum(1 for c in recent_calls if c["success"]) / len(recent_calls),
            "avg_latency_ms": sum(c["latency_ms"] for c in recent_calls) / len(recent_calls),
            "total_tokens_in": sum(c["tokens_in"] for c in recent_calls),
            "total_tokens_out": sum(c["tokens_out"] for c in recent_calls),
            "by_provider": self._group_by(recent_calls, "provider"),
            "errors": dict(self.errors)
        }
    
    def _group_by(self, calls: List[Dict], key: str) -> Dict:
        """按key分组"""
        grouped = defaultdict(list)
        for c in calls:
            grouped[c[key]].append(c)
        
        return {
            k: {
                "count": len(v),
                "avg_latency": sum(c["latency_ms"] for c in v) / len(v)
            }
            for k, v in grouped.items()
        }
    
    def save_log(self, path: str):
        """保存日志"""
        with open(path, "w") as f:
            json.dump({
                "metrics": dict(self.metrics),
                "errors": dict(self.errors)
            }, f, indent=2)
```

---

## 六、实施时间表

| Week | 任务 | 交付物 | 状态 |
|------|------|--------|------|
| Week 1 | 基础集成 | AIGateway.py | 待实施 |
| Week 2 | 成本优化 | CostController.py | 待实施 |
| Week 3 | 多模态 | MultimodalGateway.py | 待实施 |
| Week 4 | Agent编排 | AgentOrchestrator.py | 待实施 |

---

## 七、下一步行动

1. **立即行动**: 创建 `lib/ai_gateway.py` 基础框架
2. **本周完成**: 申请 OpenAI 和 Anthropic API密钥
3. **下周完成**: 实现成本控制和缓存机制
4. **持续优化**: 根据使用情况调整路由策略

---

_实施方案设计完毕 - 小龙虾分身9_