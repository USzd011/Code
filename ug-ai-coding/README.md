# UG AI 自动编程插件

> 打造运行在 **Siemens NX 12.0** 中的 AI 自动编程插件
> 实现从 **零件图纸/3D模型 → 工艺规划 → G代码生成 → 刀路仿真 → 机床验证** 的全流程自动化

## 📁 项目结构

```
ug-ai-coding/
├── cnc_core/
│   ├── __init__.py
│   ├── cutting_params.py      # 切削参数计算器 (14材料 × 10刀具)
│   ├── gcode_generator.py     # G代码生成器 (车/铣/钻/镗/攻丝)
│   ├── post_processor.py      # 后处理器 (FANUC/SIEMENS/广数)
│   ├── toolpath_simulator.py  # 刀路仿真与碰撞检测
│   ├── process_planner.py     # 工艺路线自动编排
│   ├── database.py            # SQLite 数据库层
│   └── api_server.py          # REST API 服务
├── ug_plugin/
│   └── nx12_plugin.py         # UG 12.0 插件主程序
├── test_all.py                # 完整测试套件
├── data/                      # SQLite 数据库
├── logs/                      # 运行日志
├── requirements.txt
└── README.md
```

## 🚀 快速启动

### 1. 安装依赖

```bash
pip install fastapi uvicorn pydantic
```

### 2. 运行测试

```bash
python test_all.py
```

### 3. 启动 API 服务

```bash
cd cnc_core
python api_server.py
```

服务启动后访问:
- 健康检查: `http://localhost:8000/health`
- 材料列表: `http://localhost:8000/materials`
- 刀具类型: `http://localhost:8000/tool-types`
- 切削参数: `POST http://localhost:8000/cutting-params`
- G代码生成: `POST http://localhost:8000/generate-gcode`
- 工艺编排: `POST http://localhost:8000/plan-process`
- 刀路仿真: `POST http://localhost:8000/simulate`
- 工艺方案: `GET http://localhost:8000/plans`

### 4. API 调用示例

```bash
# 计算切削参数
curl -X POST http://localhost:8000/cutting-params \
  -H "Content-Type: application/json" \
  -d '{"material": "45号钢", "tool_type": "立铣刀", "tool_diameter": 10, "operation": "roughing"}'

# 生成G代码
curl -X POST http://localhost:8000/generate-gcode \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "face_milling",
    "material": "45号钢",
    "tool_type": "面铣刀",
    "tool_diameter": 20,
    "workpiece_length": 100,
    "workpiece_width": 80,
    "workpiece_height": 15,
    "post_processor": "FANUC"
  }'
```

## 🧪 测试

```bash
python test_all.py
```

## 📋 核心功能

| 模块 | 功能 | 状态 |
|------|------|------|
| M1 | 切削参数计算 (14种材料 × 10种刀具) | ✅ |
| M2 | G代码生成 (车/铣/钻/镗/攻丝) | ✅ |
| M3 | 后处理 (FANUC/SIEMENS/广数) | ✅ |
| M4 | 刀路仿真与碰撞检测 | ✅ |
| M5 | 工艺路线自动编排 | ✅ |
| M6 | REST API 服务 | ✅ |
| M7 | SQLite 数据库 | ✅ |
| M8 | UG 12.0 插件框架 | ✅ |

## 🔧 技术栈

- **Python 3.10+**
- **FastAPI** - REST API
- **SQLite** - 数据库
- **NX Open** - UG API

## 📝 版本

- V1.0 (2026-05-22) - 初始版本
