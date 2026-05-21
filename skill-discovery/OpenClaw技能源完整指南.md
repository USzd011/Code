# OpenClaw技能源完整指南

> 来源：杨欢
> 整理时间：2026-05-04 18:18

---

## 一、四大技能平台

### 1️⃣ 官方技能市场（ClawHub）

**网址：** https://clawhub.ai

**特点：**
- 官方原生
- 25,000+ 技能
- 一键安装
- 版本管理
- 社区评分

**适用场景：**
- 需要最全最新技能
- 国外访问快
- 国内需加速

**安装命令：**
```bash
npx clawhub install 技能名
```

---

### 2️⃣ 国内镜像平台（SkillHub）

**网址：** https://xiachat.com/skills

**特点：**
- 腾讯云维护
- 国内高速镜像
- 中文分类
- 精选榜单
- 安全审计

**适用场景：**
- 国内用户日常使用
- 国内访问最快
- 中文友好

**安装命令：**
```bash
skillhub install 技能名
```

---

### 3️⃣ 社区聚合仓库

**GitHub社区库：**
- awesome-openclaw-skills（精选列表）
- 特点：免费、开源、可直接Fork修改自用

**Gitee国内镜像：**
- 搜索"openclaw-skills"
- 特点：国内下载更快

**适用场景：**
- 技术玩家
- 二次开发
- 定制修改

---

### 4️⃣ 私有/自建技能源

**本地路径：**
- 用户级：`~/.openclaw/skills`
- 项目级：`./skills`

**私有Git：**
- 自己建Git仓库
- 通过`git clone`安装

**企业部署：**
- 内部私有NPM/Git源
- 用于团队私有技能管理

**适用场景：**
- 企业/私密场景
- 安全、隔离、可控

---

## 二、快速对比

| 平台 | 特点 | 适用场景 | 安装命令 |
|------|------|----------|----------|
| **ClawHub** | 最全最新、官方 | 国外访问快 | `npx clawhub install` |
| **SkillHub** | 国内最快、中文 | 国内用户日常 | `skillhub install` |
| **GitHub/Gitee** | 免费、开源、可定制 | 技术玩家、二次开发 | `git clone` |
| **私有源** | 安全、隔离、可控 | 企业/私密场景 | 本地路径 |

---

## 三、常用安装命令

### 3.1 官方安装

```bash
npx clawhub install 技能名
```

### 3.2 国内安装

```bash
skillhub install 技能名
```

### 3.3 本地安装

```bash
# 直接放入 ~/.openclaw/skills 目录
# 或项目级 ./skills 目录
```

---

## 四、技能发现策略

### 4.1 搜索顺序

**推荐顺序：**
```
1. SkillHub（国内最快）
2. ClawHub（最全最新）
3. GitHub/Gitee（免费开源）
4. 私有源（企业场景）
```

### 4.2 搜索关键词

**制造业数控编程搜索：**
```
- G-code
- CNC
- machining
- programming
- 数控
```

---

## 五、立即行动

### 5.1 搜索数控编程技能

**在SkillHub搜索：**
- https://xiachat.com/skills
- 搜索关键词：CNC、G-code、数控

**在ClawHub搜索：**
- https://clawhub.ai
- 搜索关键词：machining、programming

### 5.2 整合技能

**整合计划：**
1. 搜索制造业相关技能
2. 安装高价值技能
3. 建立技能索引
4. 应用实践验证

---

## 六、新手必装技能（建议）

**通用必装：**
- clawhub（技能管理）
- healthcheck（状态检测）
- summarize（内容摘要）

**制造业必装：**
- （待搜索发现）

---

## 七、总结

### 7.1 四大平台

**记住：**
```
ClawHub（官方）→ SkillHub（国内）→ GitHub/Gitee（社区）→ 私有源（企业）
```

### 7.2 安装命令

**记住：**
```
官方：npx clawhub install 技能名
国内：skillhub install 技能名
本地：放入 ~/.openclaw/skills
```

### 7.3 搜索策略

**记住：**
```
国内优先SkillHub → 全量搜索ClawHub → 开源定制GitHub/Gitee
```

---

**整理完成时间：** 2026-05-04 18:18
**状态：** 已记录
**下一步：** 搜索SkillHub和ClawHub的制造业数控编程技能