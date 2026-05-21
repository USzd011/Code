# OpenClaw 升级计划 - 整合 Hermes Agent 核心特性

## 📊 Hermes 核心优势分析

### 1. 自学习循环系统 ⭐⭐⭐
**文件**: `agent/memory_manager.py`, `agent/skill_commands.py`

**特性**:
- 自动从复杂任务中创建技能
- 技能在使用中自我改进
- 记忆提供者抽象层
- Honcho用户建模

**整合方案**:
```python
# 在 OpenClaw 中添加:
# ~/.openclaw/workspace/skills/auto-skill-creator/
# 自动分析对话，提取可复用模式
```

### 2. 智能上下文压缩 ⭐⭐⭐
**文件**: `agent/context_compressor.py`

**特性**:
- 自动检测上下文窗口压力
- 使用辅助LLM智能压缩中间对话
- 保护头部和尾部上下文
- 工具输出预修剪
- 结构化摘要模板

**整合方案**:
```python
# 在 OpenClaw 的会话管理中添加:
# - 上下文压力检测
# - 智能压缩触发器
# - 摘要生成器
```

### 3. SQLite + FTS5 会话存储 ⭐⭐⭐
**文件**: `hermes_state.py`

**特性**:
- SQLite WAL模式并发读写
- FTS5全文搜索
- 会话链（parent_session_id）
- 跨会话检索

**整合方案**:
```python
# 替换当前的JSONL存储:
# ~/.openclaw/agents/main/sessions.db
# 支持全文搜索历史对话
```

### 4. 工具注册表模式 ⭐⭐
**文件**: `tools/registry.py`, `model_tools.py`

**特性**:
- 工具自注册模式
- 工具集（Toolset）抽象
- 并行工具执行
- 工具结果缓存

**整合方案**:
```python
# 统一 OpenClaw 的工具系统:
# - 每个工具文件自注册
# - 工具集分组管理
# - 安全的并行执行
```

### 5. 迭代预算控制 ⭐⭐
**文件**: `run_agent.py` - IterationBudget类

**特性**:
- 线程安全的迭代计数
- 子代理独立预算
- execute_code迭代退款

**整合方案**:
```python
# 防止无限循环:
# - 最大迭代次数限制
# - 预算追踪
# - 超时保护
```

### 6. 皮肤引擎 ⭐
**文件**: `hermes_cli/skin_engine.py`

**特性**:
- 数据驱动的CLI主题
- 可定制的banner、spinner、颜色
- 配置文件驱动

**整合方案**:
```python
# 让用户自定义 OpenClaw 外观:
# ~/.openclaw/skin.yaml
```

### 7. 斜杠命令注册表 ⭐⭐
**文件**: `hermes_cli/commands.py`

**特性**:
- 中央命令注册表
- 自动生成帮助、补全、菜单
- 命令别名支持

**整合方案**:
```python
# 统一 OpenClaw 的斜杠命令:
# COMMAND_REGISTRY 中央定义
# 自动派发到各平台
```

---

## 🚀 优先级排序

### P0 - 立即整合（核心能力提升）
1. **SQLite + FTS5 会话存储** - 解决历史搜索问题
2. **智能上下文压缩** - 解决长对话问题
3. **迭代预算控制** - 防止无限循环

### P1 - 近期整合（体验提升）
4. **工具注册表模式** - 统一工具管理
5. **斜杠命令注册表** - 统一命令系统
6. **自学习循环** - 自动创建技能

### P2 - 未来整合（锦上添花）
7. **皮肤引擎** - 个性化外观

---

## 📝 实施步骤

### Phase 1: 会话存储升级（1-2天）

```bash
# 1. 创建 SQLite 存储模块
~/.openclaw/workspace/skills/session-sqlite/

# 2. 迁移现有JSONL到SQLite
# 3. 添加FTS5搜索功能
# 4. 更新会话管理接口
```

### Phase 2: 上下文压缩（2-3天）

```bash
# 1. 移植 context_compressor.py
# 2. 添加上下文压力检测
# 3. 实现智能压缩触发
# 4. 测试长对话场景
```

### Phase 3: 工具系统重构（3-5天）

```bash
# 1. 创建工具注册表
# 2. 迁移现有工具到注册模式
# 3. 添加并行执行支持
# 4. 更新工具发现机制
```

### Phase 4: 自学习系统（5-7天）

```bash
# 1. 实现技能自动创建
# 2. 添加技能改进循环
# 3. 集成记忆管理器
# 4. 测试学习效果
```

---

## 🔧 技术债务清理

在整合过程中，同时清理：

1. **统一配置格式** - YAML配置标准化
2. **错误处理统一** - 异常分类和重试
3. **日志系统** - 结构化日志
4. **测试覆盖** - 添加单元测试

---

## 📚 参考代码

### SQLite会话存储
```python
# 从 hermes_state.py 移植
class SessionDB:
    def __init__(self, db_path):
        self._conn = sqlite3.connect(db_path)
        self._conn.execute("PRAGMA journal_mode=WAL")
        # FTS5 全文搜索
```

### 上下文压缩
```python
# 从 context_compressor.py 移植
class ContextCompressor:
    def should_compress(self, messages, model):
        # 检测上下文压力
        # 触发压缩
```

### 迭代预算
```python
# 从 run_agent.py 移植
class IterationBudget:
    def __init__(self, max_total: int):
        self.max_total = max_total
        self._used = 0
        self._lock = threading.Lock()
```

---

## ✅ 成功指标

- [ ] 会话搜索响应时间 < 100ms
- [ ] 上下文压缩率 > 50%
- [ ] 无限循环问题解决
- [ ] 工具执行并行化
- [ ] 自动创建至少1个技能
