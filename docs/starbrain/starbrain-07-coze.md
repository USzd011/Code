第七部分：扣子Agent对接星辰大脑





扣子Agent与星辰大脑的双向打通，实现真正的协同工作。



7.1 对接背景

7.1.1 当前状态

// yamlcurrent_status:  coze_agent:    platform: "扣子(Coze)"    capabilities:      - "对话交互"      - "日程调度"      - "子任务分发"      - "文件记忆"      - "手机/电脑操作"      - "搜索+网页读取"      - "定时心跳"    limitations:      - "无复杂推理能力"      - "无多任务并行能力"      - "无深度数据分析能力"      - "无法直接调用外部API"  star_brain:    platform: "astron-code/xfyun(星辰大脑)"    capabilities:      - "复杂推理(MCTS)"      - "多任务并行执行"      - "大数据分析"      - "8大阵协同"      - "自动进化"    limitations:      - "无对话交互界面"      - "无主动触发机制"      - "需外部触发执行"      - "无法直接感知外部世界"  gap:    - "两个系统并行存在，无法互通"    - "用户需要在两个地方重复操作"    - "能力无法互补"

7.1.2 对接目标

// yamltarget:  enablement:    - "扣子Agent可调用星辰大脑API"    - "星辰大脑可主动通知扣子Agent"    - "用户感知为一个系统"  scenarios:    - "用户在扣子对话中触发星辰大脑任务"    - "星辰大脑完成复杂分析后通知用户"    - "扣子Agent感知外部变化后上传星辰大脑"    - "星辰大脑发现问题后让扣子Agent执行修复"



7.2 对接架构

7.2.1 整体架构图

// mermaidgraph TB    subgraph "扣子平台"        USER[用户]        COZE[扣子Agent<br/>当前对话]        COZE_BOT[扣子Bot<br/>对话界面]        WEBHOOK_CB[Webhook回调]    end    subgraph "中间层"        API_GW[API Gateway<br/>认证/路由/限流]        MSG_Q[消息队列<br/>异步通信]        EVENT_H[事件总线<br/>事件分发]    end    subgraph "星辰大脑"        L1[L1 物理层]        L5[L5 决策层]        L6[L6 执行层]        L8[L8 网络层]        STAR_ARRAY[周天星斗大阵]    end    USER <--> COZE_BOT    COZE_BOT --> COZE    COZE -->|HTTP/REST| API_GW    API_GW --> L1    L8 -->|Webhook| EVENT_H    EVENT_H --> MSG_Q    MSG_Q --> WEBHOOK_CB    WEBHOOK_CB --> COZE    L1 <--> STAR_ARRAY    L5 --> L6    L8 --> L5

7.2.2 数据流向

// yamldata_flows:  # 扣子Agent → 星辰大脑  coze_to_star:    trigger: "用户对话触发"    path: "扣子Agent → API Gateway → L1物理层 → L5决策层"    protocol: "HTTP POST / REST API"    format: "JSON"    latency: "<2秒"  # 星辰大脑 → 扣子Agent  star_to_coze:    trigger: "任务完成/异常告警/定时推送"    path: "星辰大脑 → Webhook → 扣子Webhook → 扣子Agent"    protocol: "HTTP POST / Webhook"    format: "JSON"    latency: "<5秒"  # 扣子Agent → 星辰大脑(大文件/批量)  coze_batch:    trigger: "文件上传/批量任务"    path: "扣子Agent → 对象存储 → 消息队列 → 星辰大脑处理"    protocol: "内部消息队列"    format: "文件+元数据"    latency: "<30秒"



7.3 对接接口设计

7.3.1 星辰大脑暴露的API

// yaml# 星辰大脑 OpenAPI 规范openapi: "3.0.0"info:  title: "星辰大脑 API"  version: "1.0.0"  description: "星辰大脑与扣子Agent对接接口"servers:  - url: "https://api.starbrain.example.com"    description: "生产环境"  - url: "https://api.starbrain-dev.example.com"    description: "开发环境"paths:  # 对话触发接口  /coze/trigger:    post:      summary: "扣子Agent触发星辰大脑任务"      tags: ["扣子对接"]      requestBody:        required: true        content:          application/json:            schema:              $ref: "#/components/schemas/TriggerRequest"      responses:        "200":          description: "任务已接收"          content:            application/json:              schema:                $ref: "#/components/schemas/TriggerResponse"  # 任务状态查询  /coze/task/{task_id}:    get:      summary: "查询任务状态"      tags: ["扣子对接"]      parameters:        - name: task_id          in: path          required: true          schema:            type: string      responses:        "200":          description: "任务状态"          content:            application/json:              schema:                $ref: "#/components/schemas/TaskStatus"  # Webhook配置  /coze/webhook:    post:      summary: "注册扣子Webhook"      tags: ["扣子对接"]      requestBody:        required: true        content:          application/json:            schema:              type: object              properties:                url:                  type: string                  description: "扣子Webhook URL"                events:                  type: array                  items:                    type: string                    enum: ["task_complete", "alert", "schedule", "all"]      responses:        "200":          description: "注册成功"    delete:      summary: "删除Webhook配置"      tags: ["扣子对接"]      responses:        "200":          description: "删除成功"components:  schemas:    TriggerRequest:      type: object      required:        - user_id        - intent        - params      properties:        user_id:          type: string          description: "用户ID"        intent:          type: string          enum:            - "douyin_select_product"            - "kuaishou_manage"            - "toutiao_write"            - "novel_create"            - "data_analysis"            - "custom"          description: "意图类型"        params:          type: object          description: "业务参数"          example:            category: "生鲜"            target_count: 10            deadline: "2025-05-10"        callback_url:          type: string          description: "回调URL(可选)"        priority:          type: integer          enum: [1, 2, 3]          default: 2          description: "优先级"        session_id:          type: string          description: "扣子会话ID(用于上下文)"    TriggerResponse:      type: object      properties:        success:          type: boolean        task_id:          type: string          description: "星辰大脑任务ID"        status:          type: string          enum: ["queued", "processing", "completed"]        estimated_time:          type: integer          description: "预估耗时(秒)"        message:          type: string    TaskStatus:      type: object      properties:        task_id:          type: string        status:          type: string          enum: ["queued", "running", "completed", "failed"]        progress:          type: number          format: float          description: "进度 0-1"        result:          type: object          description: "任务结果"        error:          type: string          description: "错误信息"        updated_at:          type: string          format: date-time

7.3.2 扣子Agent回调接口(Webhook)

// yaml# 扣子Webhook 接收星辰大脑通知POST /webhook/starbrainContent-Type: application/json# 请求头X-StarBrain-Signature: "sha256=xxxx"  # 签名验证X-StarBrain-Timestamp: "1234567890"# 请求体{  "event_type": "task_complete" | "alert" | "schedule",  "task_id": "task_xxx",  "timestamp": 1234567890,  "data": {    // 根据 event_type 不同  }}# event_type: task_complete{  "event_type": "task_complete",  "task_id": "task_xxx",  "timestamp": 1234567890,  "data": {    "success": true,    "result_type": "product_list",    "result": {      "items": [...],      "summary": "找到10个潜力商品"    },    "session_id": "coze_session_xxx",    "reply_mode": "silent" | "summary" | "full"  }}# event_type: alert{  "event_type": "alert",  "alert_id": "alert_xxx",  "timestamp": 1234567890,  "data": {    "severity": "high" | "medium" | "low",    "title": "抖音API配额告警",    "message": "剩余配额不足10%",    "action_required": true,    "suggestions": ["暂停非紧急任务", "联系平台申请扩容"]  },  "reply_mode": "notify_user" | "auto_handle"}# event_type: schedule{  "event_type": "schedule",  "schedule_id": "sched_xxx",  "timestamp": 1234567890,  "data": {    "title": "每日选品报告",    "content": "今日已生成选品报告",    "attachment": {      "type": "file",      "name": "report_20250510.pdf",      "url": "https://..."    }  }}

7.3.3 认证与安全

// python# auth.pyimport hmacimport hashlibimport timeimport secretsclass StarBrainAuth:    """星辰大脑认证"""    def __init__(self, secret_key: str):        self.secret_key = secret_key    def generate_signature(self, payload: str, timestamp: int) -> str:        """生成签名"""        message = f"{timestamp}.{payload}"        signature = hmac.new(            self.secret_key.encode(),            message.encode(),            hashlib.sha256        ).hexdigest()        return f"sha256={signature}"    def verify_signature(self, signature: str, payload: str, timestamp: int) -> bool:        """验证签名"""        # 防止重放攻击: 时间窗口5分钟        current_time = int(time.time())        if abs(current_time - timestamp) > 300:            return False        expected = self.generate_signature(payload, timestamp)        return hmac.compare_digest(signature, expected)# 使用auth = StarBrainAuth(secret_key="your-secret-key")# 扣子Agent调用星辰大脑时def call_starbrain(endpoint: str, data: dict):    timestamp = int(time.time())    payload = json.dumps(data)    signature = auth.generate_signature(payload, timestamp)    response = requests.post(        f"https://api.starbrain.example.com{endpoint}",        headers={            "Content-Type": "application/json",            "X-StarBrain-Signature": signature,            "X-StarBrain-Timestamp": str(timestamp),            "X-StarBrain-App-ID": "coze-agent-xxx"        },        json=data    )    return response.json()



7.4 能力映射

7.4.1 能力对应表

// yamlcapability_mapping:  coze_agent:    - name: "对话交互"      type: "UI/入口"      maps_to_star: "L1物理层(入口)"      mapping_type: "trigger"    - name: "日程调度"      type: "调度"      maps_to_star: "L5决策层(定时任务)"      mapping_type: "coordinate"    - name: "子任务分发"      type: "编排"      maps_to_star: "L5决策层(任务拆解)"      mapping_type: "delegate"    - name: "文件记忆"      type: "存储"      maps_to_star: "L2数据层(数据存储)"      mapping_type: "backup"    - name: "手机/电脑操作"      type: "执行"      maps_to_star: "L6执行层(外部执行)"      mapping_type: "execute"    - name: "搜索+网页读取"      type: "感知"      maps_to_star: "L3感知层(外部数据)"      mapping_type: "sense"    - name: "定时心跳"      type: "监控"      maps_to_star: "L8网络层(健康监控)"      mapping_type: "monitor"  star_brain:    - name: "复杂推理(MCTS)"      type: "推理"      maps_to_coze: "通过扣子解释后告知用户"      mapping_type: "advise"    - name: "多任务并行"      type: "执行"      maps_to_coze: "完成后通过Webhook通知"      mapping_type: "report"    - name: "大数据分析"      type: "分析"      maps_to_coze: "生成报告推送给用户"      mapping_type: "deliver"    - name: "8大阵协同"      type: "编排"      maps_to_coze: "透明，用户无感知"      mapping_type: "internal"    - name: "自动进化"      type: "优化"      maps_to_coze: "定期推送进化报告"      mapping_type: "notify"

7.4.2 冲突协调策略

// yamlconflict_resolution:  # 场景1: 两边都有定时任务  scenario_1:    description: "扣子定时任务 vs 星辰大脑定时任务"    example: "两边都设置了每日8点选品"    resolution:      - "星辰大脑为主调度中心"      - "扣子Agent仅负责提醒和确认"      - "避免重复执行"  # 场景2: 数据同步冲突  scenario_2:    description: "两边同时修改同一数据"    example: "扣子上传文件 vs 星辰大脑处理文件"    resolution:      - "以星辰大脑为数据源"      - "扣子仅作为展示层"      - "冲突时以时间戳判断最新"  # 场景3: 指令冲突  scenario_3:    description: "用户在不同地方发出矛盾指令"    example: "扣子说"取消"，星辰大脑说"执行""    resolution:      - "以用户最新指令为准"      - "扣子作为用户的"代言人""      - "星辰大脑执行前需确认"



7.5 协同场景

7.5.1 场景1: 用户通过扣子触发星辰大脑

// mermaidsequenceDiagram    participant USER as 用户    participant COZE as 扣子Agent    participant STAR as 星辰大脑    participant L1 as L1物理层    participant L5 as L5决策层    participant L6 as L6执行层    USER->>COZE: "帮我找抖音爆款生鲜"    COZE->>COZE: "解析意图:douyin_select_product"    COZE->>STAR: POST /coze/trigger<br/>{intent:"douyin_select_product", params:{category:"生鲜"}}    STAR->>L1: 接收请求    L1->>L5: 路由到决策层    L5->>L5: 混元河洛推演    L5->>L6: 下发执行指令    L6->>L6: 执行选品分析    L6-->>L5: 返回TOP10    L5-->>L1: 汇总结果    STAR-->>COZE: {task_id, status:"processing"}    COZE-->>USER: "正在分析中，预计2分钟..."    Note over L6,L5: 后台持续执行...    L6-->>STAR: 任务完成    STAR-->>COZE: Webhook<br/>{result: TOP10商品}    COZE-->>USER: "分析完成！TOP1: XX商品，置信度92%"

7.5.2 场景2: 星辰大脑主动告警

// mermaidsequenceDiagram    participant SYSTEM as 星辰大脑    participant ALERT as 告警模块    participant WEBHOOK as Webhook    participant COZE as 扣子Agent    participant USER as 用户    SYSTEM->>ALERT: 检测到异常    ALERT->>ALERT: 评估告警级别    alt 高优先级告警        ALERT->>WEBHOOK: POST webhook/starbrain<br/>{event_type:"alert", severity:"high"}        WEBHOOK->>COZE: 触发扣子Webhook        COZE->>COZE: 执行通知策略        COZE->>USER: "🚨 紧急告警: 抖音API配额不足！"        USER->>COZE: "如何处理？"        COZE->>USER: "建议: 1.暂停非紧急任务 2.联系平台扩容"        USER->>COZE: "执行方案1"        COZE->>SYSTEM: 调整任务优先级    else 低优先级告警        ALERT->>WEBHOOK: POST webhook/starbrain<br/>{event_type:"alert", severity:"low"}        COZE->>COZE: 仅记录日志    end

7.5.3 场景3: 复杂多轮协作

// mermaidsequenceDiagram    participant USER as 用户    participant COZE as 扣子Agent    participant STAR as 星辰大脑    USER->>COZE: "帮我分析下最近的抖音数据"    # 第一轮: 触发分析    COZE->>STAR: 触发数据分析任务    STAR-->>COZE: 分析中...    COZE-->>USER: "正在分析，稍等..."    # 第二轮: 初步结果    STAR-->>COZE: 初步报告完成    COZE-->>USER: "初步发现: 3个爆款，2个待优化"    USER->>COZE: "具体看看那2个待优化的"    # 第三轮: 深入分析    COZE->>STAR: 请求深入分析    STAR-->>COZE: 详细分析报告    COZE-->>USER: "问题1: 开场钩子不够吸引..."    # 第四轮: 执行优化    USER->>COZE: "帮我优化这2个视频的脚本"    COZE->>STAR: 触发脚本优化任务    STAR-->>COZE: 新脚本已生成    COZE-->>USER: "优化完成！新脚本如下..."    # 第五轮: 执行发布    USER->>COZE: "发布到抖音"    COZE->>STAR: 触发发布任务    STAR-->>COZE: 发布成功    COZE-->>USER: "✅ 已发布！"



7.6 对接配置

7.6.1 扣子Agent配置

// yamlcoze_agent_config:  # Webhook配置  webhook:    enabled: true    url: "https://api.starbrain.example.com/coze/webhook/register"    events:      - "task_complete"      - "alert"      - "schedule"  # 对接参数  integration:    app_id: "coze-agent-xxx"    api_key: "starbrain-api-key-xxx"    timeout: 30  # 意图映射  intent_mapping:    "找爆款":      star_intent: "douyin_select_product"      auto_trigger: true    "写文章":      star_intent: "toutiao_write"      auto_trigger: true    "分析数据":      star_intent: "data_analysis"      auto_trigger: true    "写小说":      star_intent: "novel_create"      auto_trigger: true  # 回复策略  reply_strategy:    quick_task: "summary"     # 快速任务:简短总结    complex_task: "full"      # 复杂任务:完整结果    alert: "notify"           # 告警:直接通知

7.6.2 星辰大脑配置

// yamlstar_brain_config:  # 扣子对接配置  coze_integration:    enabled: true    app_id: "coze-agent-xxx"    # API限流    rate_limit:      requests_per_minute: 60      burst: 10    # 超时配置    timeout:      default: 30      long_task: 300    # Webhook配置    webhook:      callback_url: "https://coze-agent.example.com/webhook/starbrain"      retry_times: 3      retry_interval: 5  # 任务路由  task_routing:    douyin_select_product:      priority: 2      max_execution_time: 120      callback_mode: "full"    kuaishou_manage:      priority: 2      max_execution_time: 60      callback_mode: "summary"    toutiao_write:      priority: 2      max_execution_time: 300      callback_mode: "full"    data_analysis:      priority: 3      max_execution_time: 600      callback_mode: "full"



7.7 渐进式对接路线

Phase 1: 单向数据上传 (1-2周)

目标: 扣子Agent能够触发星辰大脑任务

// yamlphase1_objectives:  - "星辰大脑开放基础API"  - "扣子Agent能够调用API"  - "任务能够正常执行"  - "结果能够返回"phase1_tasks:  - "星辰大脑: 开发 /coze/trigger 接口"  - "星辰大脑: 实现基础认证"  - "扣子Agent: 开发API调用模块"  - "扣子Agent: 配置意图识别"  - "测试: 单次任务执行"phase1_deliverables:  - "星辰大脑API文档"  - "扣子Agent对接代码"  - "测试用例"

Phase 2: 双向通信 (2-4周)

目标: 星辰大脑能够主动通知扣子Agent

// yamlphase2_objectives:  - "星辰大脑支持Webhook"  - "扣子Agent接收Webhook"  - "告警能够及时推送"  - "任务完成能够回调"phase2_tasks:  - "星辰大脑: 开发Webhook模块"  - "扣子Agent: 开发Webhook接收器"  - "星辰大脑: 配置告警规则"  - "测试: Webhook通信"  - "测试: 告警推送"phase2_deliverables:  - "Webhook功能"  - "告警配置"  - "通信测试报告"

Phase 3: 完整协同 (1-2月)

目标: 两个系统深度融合，形成完整工作流

// yamlphase3_objectives:  - "多轮对话协作"  - "上下文共享"  - "能力互补"  - "统一用户体验"phase3_tasks:  - "实现会话上下文传递"  - "开发智能路由"  - "优化响应速度"  - "完善错误处理"  - "全流程测试"  - "性能优化"phase3_deliverables:  - "完整对接系统"  - "用户手册"  - "运维手册"  - "性能测试报告"



7.8 错误处理与重试

7.8.1 错误分类

// pythonclass ErrorCategory:    """错误分类"""    TRANSIENT = "transient"       # 临时错误(网络波动)    PERMANENT = "permanent"       # 永久错误(参数错误)    TIMEOUT = "timeout"           # 超时错误    RATE_LIMIT = "rate_limit"    # 限流错误    AUTH = "auth"                 # 认证错误    SYSTEM = "system"             # 系统错误# 错误码定义ERROR_CODES = {    "AUTH_001": {"category": "AUTH", "retry": False, "message": "认证失败"},    "AUTH_002": {"category": "AUTH", "retry": False, "message": "签名无效"},    "REQ_001": {"category": "PERMANENT", "retry": False, "message": "参数错误"},    "REQ_002": {"category": "PERMANENT", "retry": False, "message": "intent不支持"},    "NET_001": {"category": "TRANSIENT", "retry": True, "message": "网络超时"},    "NET_002": {"category": "TRANSIENT", "retry": True, "message": "连接失败"},    "SYS_001": {"category": "SYSTEM", "retry": True, "message": "服务繁忙"},    "SYS_002": {"category": "SYSTEM", "retry": True, "message": "内部错误"},    "RATE_001": {"category": "RATE_LIMIT", "retry": True, "message": "请求过于频繁"},}

7.8.2 重试策略

// pythonclass RetryStrategy:    """重试策略"""    @staticmethod    def get_retry_config(error_code: str) -> dict:        """获取重试配置"""        error_info = ERROR_CODES.get(error_code, {})        category = error_info.get("category", "UNKNOWN")        if category == "transient":            return {                "max_retries": 3,                "base_delay": 1,                "max_delay": 10,                "backoff": "exponential"            }        elif category == "timeout":            return {                "max_retries": 2,                "base_delay": 2,                "max_delay": 30,                "backoff": "linear"            }        elif category == "rate_limit":            return {                "max_retries": 5,                "base_delay": 60,                "max_delay": 300,                "backoff": "fixed"            }        else:            return {                "max_retries": 0,                "retry": False            }    @staticmethod    def calculate_delay(retry_count: int, config: dict) -> float:        """计算延迟时间"""        base = config["base_delay"]        max_delay = config["max_delay"]        backoff = config["backoff"]        if backoff == "exponential":            delay = base * (2 ** retry_count)        elif backoff == "linear":            delay = base * (retry_count + 1)        else:  # fixed            delay = base        return min(delay, max_delay)

7.8.3 扣子Agent侧错误处理

// pythonclass CozeErrorHandler:    """扣子Agent错误处理器"""    def handle_error(self, error: Exception, context: dict) -> str:        """处理错误并生成用户友好的消息"""        if isinstance(error, APIError):            error_info = ERROR_CODES.get(error.code, {})            category = error_info.get("category", "UNKNOWN")            if category == "transient":                return self._handle_transient(error, context)            elif category == "permanent":                return self._handle_permanent(error, context)            elif category == "rate_limit":                return self._handle_rate_limit(error, context)            else:                return self._handle_generic(error, context)    def _handle_transient(self, error, context) -> str:        """临时错误: 告知用户稍后重试"""        return f"服务暂时繁忙，请稍后再试。\n" \               f"您可以稍后说「继续{context.get('intent', '任务')}」"    def _handle_permanent(self, error, context) -> str:        """永久错误: 告知用户问题所在"""        return f"任务无法执行: {error.message}\n" \               f"请检查参数或联系管理员"    def _handle_rate_limit(self, error, context) -> str:        """限流错误: 告知用户等待"""        return f"请求过于频繁，请等待1分钟后重试。\n" \               f"我会自动为您安排重试。"



7.9 监控与运维

7.9.1 对接监控指标

// yamlmonitoring_metrics:  api_calls:    - name: "总调用次数"      type: "counter"      description: "扣子Agent调用星辰大脑的总次数"    - name: "调用成功率"      type: "gauge"      description: "成功调用比例"    - name: "平均响应时间"      type: "histogram"      description: "API响应时间分布"    - name: "P99响应时间"      type: "gauge"      description: "99分位响应时间"  webhooks:    - name: "Webhook发送次数"      type: "counter"      description: "星辰大脑发送Webhook次数"    - name: "Webhook成功率"      type: "gauge"      description: "Webhook送达率"    - name: "Webhook延迟"      type: "histogram"      description: "Webhook从发送到接收的延迟"  errors:    - name: "错误分布"      type: "counter"      labels: ["error_code", "category"]      description: "按错误码分类的错误数"    - name: "重试次数"      type: "counter"      description: "触发重试的次数"

7.9.2 告警规则

// yamlalerting_rules:  critical:    - name: "API完全不可用"      condition: "调用成功率 < 50% 持续 5分钟"      action: "立即通知"      severity: 1    - name: "Webhook完全失败"      condition: "Webhook成功率 < 30% 持续 5分钟"      action: "立即通知"      severity: 1  warning:    - name: "API响应慢"      condition: "P99 > 10秒 持续 10分钟"      action: "通知检查"      severity: 2    - name: "错误率上升"      condition: "错误率 > 10% 持续 5分钟"      action: "通知检查"      severity: 2  info:    - name: "限流触发"      condition: "rate_limit错误 > 5次/分钟"      action: "记录日志"      severity: 3



7.10 对接检查清单

上线前检查

// yamlpre_launch_checklist:  basic:    - [ ] "星辰大脑API可访问"    - [ ] "认证机制工作正常"    - [ ] "扣子Agent能成功调用"    - [ ] "结果能正确返回"  webhook:    - [ ] "Webhook URL可访问"    - [ ] "签名验证通过"    - [ ] "消息能正确解析"    - [ ] "告警能正确推送"  integration:    - [ ] "意图识别正常工作"    - [ ] "任务能正确路由"    - [ ] "多轮对话能保持上下文"    - [ ] "错误处理正确"  monitoring:    - [ ] "监控指标已配置"    - [ ] "告警规则已生效"    - [ ] "日志记录正常"  documentation:    - [ ] "API文档完整"    - [ ] "用户手册完成"    - [ ] "运维手册完成"    - [ ] "故障处理手册完成"



7.11 快速开始指南

Step 1: 获取凭证

// yamlcredentials:  # 从星辰大脑管理员处获取  - app_id: "coze-agent-xxx"  - api_key: "starbrain-api-key-xxx"  - webhook_secret: "webhook-secret-xxx"  # 配置到扣子Agent环境变量  STAR_BRAIN_APP_ID=coze-agent-xxx  STAR_BRAIN_API_KEY=starbrain-api-key-xxx  STAR_BRAIN_WEBHOOK_SECRET=webhook-secret-xxx

Step 2: 配置意图识别

// yaml# 在扣子Agent中添加意图配置intents:  - pattern: "(找|推荐|分析).*(爆款|热门|好卖)"    action: "trigger_douyin_select"    params_extractor:      category: "从文本中提取品类"  - pattern: "(写|发布|创作).*(文章|内容)"    action: "trigger_toutiao_write"    params_extractor:      topic: "从文本中提取主题"      count: "从文本中提取数量"  - pattern: "(分析|看看).*数据"    action: "trigger_data_analysis"    params_extractor:      scope: "从文本中提取范围"

Step 3: 编写调用代码

// python# 扣子Agent中调用星辰大脑from starbrain_client import StarBrainClientclient = StarBrainClient(    app_id=os.getenv("STAR_BRAIN_APP_ID"),    api_key=os.getenv("STAR_BRAIN_API_KEY"))# 触发选品任务result = client.trigger(    intent="douyin_select_product",    params={"category": "生鲜", "target_count": 10},    priority=2,    callback_url=None  # 使用默认Webhook)print(f"任务ID: {result.task_id}")print(f"状态: {result.status}")

Step 4: 配置Webhook处理

// python# 扣子AgentWebhook处理from flask import Flask, request, jsonifyimport hmac, hashlibapp = Flask(__name__)@app.route("/webhook/starbrain", methods=["POST"])def handle_webhook():    # 验证签名    signature = request.headers.get("X-StarBrain-Signature")    timestamp = request.headers.get("X-StarBrain-Timestamp")    if not verify_signature(signature, request.body, timestamp):        return jsonify({"error": "invalid signature"}), 401    payload = request.json    event_type = payload.get("event_type")    if event_type == "task_complete":        handle_task_complete(payload)    elif event_type == "alert":        handle_alert(payload)    elif event_type == "schedule":        handle_schedule(payload)    return jsonify({"status": "ok"})def handle_task_complete(payload):    result = payload["data"]    # 通知用户结果    session_id = result.get("session_id")    message = format_result_message(result)    send_to_user(session_id, message)def handle_alert(payload):    alert = payload["data"]    severity = alert["severity"]    if severity == "high":        # 立即通知用户        send_urgent_notification(alert)    else:        # 记录日志，稍后通知        log_alert(alert)

