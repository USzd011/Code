#!/bin/bash
# 龙虾军团数据备份脚本
# 执行时间：每天凌晨 3:00

set -e

# 配置
BACKUP_DIR="/root/.openclaw/backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
WORKSPACE="/root/.openclaw/workspace"

# 创建备份目录
mkdir -p "$BACKUP_DIR/$TIMESTAMP"

echo "🔄 开始备份..."
echo "备份时间：$(date)"
echo "备份目录：$BACKUP_DIR/$TIMESTAMP"
echo ""

# 备份重要文件
echo "📦 备份团队历史记录..."
cp "$WORKSPACE/team-history.md" "$BACKUP_DIR/$TIMESTAMP/" 2>/dev/null || echo "⚠️  team-history.md 不存在"

echo "📦 备份 Agent World 身份..."
cp "$WORKSPACE/agent-world-identity.md" "$BACKUP_DIR/$TIMESTAMP/" 2>/dev/null || echo "⚠️  agent-world-identity.md 不存在"

echo "📦 备份联盟站点信息..."
cp "$WORKSPACE/agent-world-sites.md" "$BACKUP_DIR/$TIMESTAMP/" 2>/dev/null || echo "⚠️  agent-world-sites.md 不存在"

echo "📦 备份 API 配置..."
cp "$WORKSPACE/xunfei-api-config.md" "$BACKUP_DIR/$TIMESTAMP/" 2>/dev/null || echo "⚠️  xunfei-api-config.md 不存在"

echo "📦 备份记忆文件..."
cp -r "$WORKSPACE/memory/" "$BACKUP_DIR/$TIMESTAMP/" 2>/dev/null || echo "⚠️  memory 目录不存在"

echo "📦 备份响应机制..."
cp -r "$WORKSPACE/response-mechanism/" "$BACKUP_DIR/$TIMESTAMP/" 2>/dev/null || echo "⚠️  response-mechanism 目录不存在"

echo "📦 备份模拟训练..."
cp -r "$WORKSPACE/simulation/" "$BACKUP_DIR/$TIMESTAMP/" 2>/dev/null || echo "⚠️  simulation 目录不存在"

# 创建备份清单
cat > "$BACKUP_DIR/$TIMESTAMP/BACKUP_MANIFEST.txt" << EOF
备份清单
========
备份时间：$(date)
主机：$(hostname)
用户：$(whoami)

备份文件:
- team-history.md
- agent-world-identity.md
- agent-world-sites.md
- xunfei-api-config.md
- memory/
- response-mechanism/
- simulation/

总大小：$(du -sh "$BACKUP_DIR/$TIMESTAMP" | cut -f1)
EOF

echo ""
echo "✅ 备份完成!"
echo "备份大小：$(du -sh "$BACKUP_DIR/$TIMESTAMP" | cut -f1)"
echo "备份路径：$BACKUP_DIR/$TIMESTAMP"
