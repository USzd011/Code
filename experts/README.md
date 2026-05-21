# 专家分身系统 - 系统总控

## 系统状态

**版本：** 1.0.0
**创建时间：** 2026-04-27
**状态：** 已搭建，待测试

## 专家清单

| 专家名称 | 配置文件 | 状态 | 核心能力 |
|---------|---------|------|---------|
| 文案专家 | copywriting-expert.yaml | ✅ 已配置 | 文案创作、爆款模板 |
| 脚本专家 | script-expert.yaml | ✅ 已配置 | 视频脚本、热点分析 |
| 视频专家 | video-expert.yaml | ✅ 已配置 | AI视频、剪辑特效 |
| 图片专家 | image-expert.yaml | ✅ 已配置 | AI绘画、海报设计 |
| 运营专家 | operation-expert.yaml | ✅ 已配置 | 排期管理、数据分析 |
| 技术专家 | tech-expert.yaml | ✅ 已配置 | 自动化、API集成 |
| 数据专家 | data-expert.yaml | ✅ 已配置 | 流量分析、用户画像 |
| 审计专家 | audit-expert.yaml | ✅ 已配置 | 成果验收、质量检查 |

## 目录结构

```
workspace/
├── experts/                    # 专家配置目录
│   ├── README.md              # 系统总控（本文件）
│   ├── copywriting-expert.yaml
│   ├── script-expert.yaml
│   ├── video-expert.yaml
│   ├── image-expert.yaml
│   ├── operation-expert.yaml
│   ├── tech-expert.yaml
│   └── data-expert.yaml
│
├── content/                    # 专家产出库
│   ├── copywriting/           # 文案库
│   │   ├── short-video/       # 短视频文案
│   │   ├── marketing/         # 营销文案
│   │   └── templates/         # 爆款模板
│   ├── scripts/               # 脚本库
│   │   ├── short-video/       # 短视频脚本
│   │   ├── comic/             # 漫剧脚本
│   │   └── topics/            # 选题库
│   ├── videos/                # 视频库
│   │   ├── finished/          # 成品
│   │   ├── drafts/            # 草稿
│   │   └── assets/            # 素材
│   ├── images/                # 图片库
│   │   ├── covers/            # 封面
│   │   ├── posters/           # 海报
│   │   └── templates/         # 设计模板
│   └── reports/               # 报告库
│       ├── operations/        # 运营报告
│       ├── data/              # 数据报告
│       └── strategies/        # 策略建议
│
├── ai-script-generator/        # AI脚本生成器
└── expert-agent-system.md      # 系统设计文档
```

## 使用方法

### 1. 查看专家配置
```bash
# 查看文案专家配置
cat experts/copywriting-expert.yaml

# 查看脚本专家配置
cat experts/script-expert.yaml
```

### 2. 调用专家工作
```javascript
// 调用文案专家
const copywritingExpert = require('./experts/copywriting-expert');
const result = await copywritingExpert.generate({
  type: '短视频文案',
  platform: '抖音',
  topic: '效率提升技巧'
});

// 调用脚本专家
const scriptExpert = require('./experts/script-expert');
const script = await scriptExpert.generate({
  type: '知识科普类',
  topic: '3个效率技巧',
  duration: 45
});
```

### 3. 查看产出库
```bash
# 查看文案产出
ls content/copywriting/

# 查看脚本产出
ls content/scripts/

# 查看视频产出
ls content/videos/
```

## 专家协作流程

### 短视频生产流程
```
脚本专家 → 文案专家 → 图片专家 → 视频专家 → 运营专家
   ↓          ↓          ↓          ↓          ↓
 生成脚本   优化文案   制作封面   生成视频   发布运营
```

### 数据驱动流程
```
数据专家 → 运营专家 → 脚本专家
   ↓          ↓          ↓
 分析数据   制定策略   优化选题
```

## 下一步

1. **测试专家配置** - 验证各专家配置是否正确
2. **测试产出流程** - 测试从需求到产出的完整流程
3. **测试专家协作** - 测试多专家协作流程
4. **优化系统** - 根据测试结果优化配置

---

**系统搭建完成，等待测试指令**