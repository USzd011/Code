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
