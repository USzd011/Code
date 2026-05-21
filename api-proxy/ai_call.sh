#!/bin/bash
# 简单的API代理脚本
# 无需安装额外依赖，直接使用curl

# API配置
GITHUB_API="https://models.inference.ai.azure.com/chat/completions"
GITHUB_TOKEN="[GITHUB_TOKEN]"

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示帮助
show_help() {
    echo "统一LLM API代理脚本"
    echo ""
    echo "用法: $0 [选项] <提示词>"
    echo ""
    echo "选项:"
    echo "  -m, --model     指定模型 (默认: gpt-4o-mini)"
    echo "  -p, --provider  指定provider (默认: github)"
    echo "  -h, --help      显示帮助"
    echo ""
    echo "可用模型:"
    echo "  - gpt-4.1 (最新，推荐)"
    echo "  - gpt-4o (高质量)"
    echo "  - gpt-4o-mini (快速)"
    echo "  - DeepSeek-V3-0324 (中文优化)"
    echo "  - Llama-4-Scout-17B-16E-Instruct (开源)"
    echo ""
    echo "示例:"
    echo "  $0 '你好'"
    echo "  $0 -m gpt-4o '写一段代码'"
    echo "  $0 -m DeepSeek-V3-0324 '解释什么是AI'"
}

# 调用API
call_api() {
    local model=$1
    local prompt=$2
    
    echo -e "${BLUE}调用模型: $model${NC}"
    echo -e "${BLUE}提示词: $prompt${NC}"
    echo ""
    
    response=$(curl -s -X POST "$GITHUB_API" \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"model\": \"$model\", \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}]}")
    
    # 提取响应内容
    content=$(echo "$response" | jq -r '.choices[0].message.content' 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$content" ] && [ "$content" != "null" ]; then
        echo -e "${GREEN}响应:${NC}"
        echo "$content"
        echo ""
        
        # 显示token使用情况
        prompt_tokens=$(echo "$response" | jq -r '.usage.prompt_tokens' 2>/dev/null)
        completion_tokens=$(echo "$response" | jq -r '.usage.completion_tokens' 2>/dev/null)
        total_tokens=$(echo "$response" | jq -r '.usage.total_tokens' 2>/dev/null)
        
        if [ -n "$prompt_tokens" ] && [ "$prompt_tokens" != "null" ]; then
            echo -e "${BLUE}Token使用: 输入=$prompt_tokens, 输出=$completion_tokens, 总计=$total_tokens${NC}"
        fi
    else
        echo "❌ 调用失败"
        echo "$response"
    fi
}

# 主函数
main() {
    local model="gpt-4o-mini"
    local prompt=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -m|--model)
                model="$2"
                shift 2
                ;;
            -p|--provider)
                # 暂时只支持github
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                prompt="$1"
                shift
                ;;
        esac
    done
    
    # 检查是否有提示词
    if [ -z "$prompt" ]; then
        echo "❌ 错误: 请提供提示词"
        echo ""
        show_help
        exit 1
    fi
    
    # 调用API
    call_api "$model" "$prompt"
}

# 运行
main "$@"
