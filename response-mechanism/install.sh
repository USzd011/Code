#!/bin/bash
# 团队响应机制安装脚本

echo "🦞 团队响应机制安装开始..."

# 创建响应机制目录
mkdir -p ~/.openclaw/workspace/response-mechanism

# 创建响应机制配置
cat > ~/.openclaw/workspace/response-mechanism/config.json << 'EOF'
{
  "version": "1.0",
  "rules": {
    "command": {
      "prefix": "（指令）",
      "responseTime": "< 1分钟",
      "action": "立即执行"
    },
    "broadcast": {
      "prefix": "@_all",
      "responseTime": "< 5分钟",
      "action": "所有成员响应"
    },
    "mention": {
      "prefix": "@特定成员",
      "responseTime": "< 10分钟",
      "action": "该成员优先响应"
    }
  },
  "escalation": {
    "timeout": "10分钟",
    "escalateTo": "Orchestrator"
  }
}
EOF

# 创建响应脚本
cat > ~/.openclaw/workspace/response-mechanism/respond.sh << 'EOF'
#!/bin/bash
# 响应消息

MESSAGE="$1"
SENDER="$2"

# 检查消息类型
if [[ "$MESSAGE" == *"（指令）"* ]]; then
  echo "⚡ 最高优先级指令，立即执行"
  # 触发立即执行
elif [[ "$MESSAGE" == *"@_all"* ]]; then
  echo "📢 团队广播，所有成员响应"
  # 触发团队响应
elif [[ "$MESSAGE" == *"@"* ]]; then
  echo "👤 特定成员响应"
  # 触发特定成员响应
fi
EOF

chmod +x ~/.openclaw/workspace/response-mechanism/respond.sh

echo "✅ 响应机制安装完成！"
echo ""
echo "📋 响应规则："
echo "  （指令）→ 立即执行（< 1分钟）"
echo "  @_all   → 所有成员响应（< 5分钟）"
echo "  @成员   → 该成员响应（< 10分钟）"
echo ""
echo "⏰ 升级机制：卡住超过10分钟自动升级"
