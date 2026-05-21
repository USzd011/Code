#!/bin/bash
# AI开发方法论 - 核心脚本
# 版本: 1.0.0
# 创建时间: 2026-05-04

# ==================== 拉尔夫循环 ====================

ralph_loop() {
    echo "🦞 启动拉尔夫循环..."
    echo "任务文件: $1"
    echo "按 Ctrl+C 停止"
    echo ""

    while :; do
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 执行任务..."
        cat "$1" | claude-code

        # 检查是否成功
        if [ $? -eq 0 ]; then
            echo "✅ 任务完成"
            break
        fi

        echo "⚠️ 任务失败，继续迭代..."
        sleep 2
    done
}

# ==================== 项目初始化 ====================

init_project() {
    local project_name=$1

    echo "🦞 初始化项目: $project_name"

    # 创建项目目录
    mkdir -p "$project_name"
    cd "$project_name"

    # 创建核心文件
    cat > PROMPT.md << 'EOF'
# 任务描述

## 目标
[清晰定义最终目标]

## 验收标准
- [ ] 标准1
- [ ] 标准2
- [ ] 标准3

## 约束条件
[设定约束条件]

## 任务列表
1. 任务1
2. 任务2
3. 任务3
EOF

    cat > agents.md << 'EOF'
# 项目长期记忆

## 项目概述
[项目基本信息]

## 关键决策
[重要决策记录]

## 经验总结
[经验教训积累]
EOF

    touch progress.txt

    echo "✅ 项目初始化完成"
    echo ""
    echo "文件结构:"
    echo "  $project_name/"
    echo "  ├── PROMPT.md      (任务描述)"
    echo "  ├── agents.md      (长期记忆)"
    echo "  └── progress.txt   (短期记忆)"
}

# ==================== 任务管理 ====================

add_task() {
    local task_name=$1
    local task_desc=$2

    echo "### 任务: $task_name" >> PROMPT.md
    echo "$task_desc" >> PROMPT.md
    echo "" >> PROMPT.md

    echo "✅ 任务已添加: $task_name"
}

list_tasks() {
    echo "📋 任务列表:"
    grep -E "^### 任务:" PROMPT.md || echo "无任务"
}

# ==================== 记忆管理 ====================

save_progress() {
    local progress=$1

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $progress" >> progress.txt
    echo "✅ 进度已保存"
}

show_progress() {
    echo "📊 进度记录:"
    cat progress.txt
}

save_knowledge() {
    local knowledge=$1

    echo "" >> agents.md
    echo "## $(date '+%Y-%m-%d')"
    echo "$knowledge" >> agents.md

    echo "✅ 知识已保存到长期记忆"
}

# ==================== 数据分析 ====================

analyze_iterations() {
    echo "📈 迭代分析:"

    # 统计迭代次数
    local iterations=$(grep -c "执行任务" progress.txt 2>/dev/null || echo 0)
    echo "  总迭代次数: $iterations"

    # 统计成功次数
    local successes=$(grep -c "任务完成" progress.txt 2>/dev/null || echo 0)
    echo "  成功次数: $successes"

    # 计算成功率
    if [ $iterations -gt 0 ]; then
        local rate=$(echo "scale=2; $successes * 100 / $iterations" | bc)
        echo "  成功率: ${rate}%"
    fi
}

# ==================== 主菜单 ====================

show_help() {
    cat << 'EOF'
🦞 AI开发方法论 - 使用指南

用法:
  ./ai_dev_method.sh <命令> [参数]

命令:
  init <项目名>           初始化新项目
  loop <任务文件>         启动拉尔夫循环
  add-task <名称> <描述>  添加任务
  list-tasks              列出所有任务
  save-progress <内容>    保存进度
  show-progress           显示进度
  save-knowledge <内容>   保存知识
  analyze                 分析迭代数据
  help                    显示帮助

示例:
  ./ai_dev_method.sh init my_project
  ./ai_dev_method.sh loop PROMPT.md
  ./ai_dev_method.sh add-task "实现登录功能" "用户登录验证"
  ./ai_dev_method.sh save-progress "完成登录功能开发"
  ./ai_dev_method.sh analyze

核心理念:
  - 流程 > 模型
  - 拥抱失败，无限迭代
  - 一切不为我所有，但是为我所用

EOF
}

# ==================== 主程序 ====================

case "$1" in
    init)
        init_project "$2"
        ;;
    loop)
        ralph_loop "$2"
        ;;
    add-task)
        add_task "$2" "$3"
        ;;
    list-tasks)
        list_tasks
        ;;
    save-progress)
        save_progress "$2"
        ;;
    show-progress)
        show_progress
        ;;
    save-knowledge)
        save_knowledge "$2"
        ;;
    analyze)
        analyze_iterations
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        echo "使用 './ai_dev_method.sh help' 查看帮助"
        exit 1
        ;;
esac