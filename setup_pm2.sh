#!/bin/bash
# OpenClaw PM2 后台运行配置
# 使用方法: bash setup_pm2.sh

set -e

echo "🦞 配置 OpenClaw 后台运行..."

# 1. 安装 PM2
echo "📦 安装 PM2..."
npm install -g pm2

# 2. 创建启动脚本
echo "📝 创建启动脚本..."
cat > /root/start_openclaw.sh << 'EOF'
#!/bin/bash
cd /root
openclaw gateway start
EOF
chmod +x /root/start_openclaw.sh

# 3. 启动 OpenClaw Gateway
echo "🚀 启动 OpenClaw Gateway..."
pm2 delete openclaw-gateway 2>/dev/null || true
pm2 start /root/start_openclaw.sh --name openclaw-gateway --interpreter bash

# 4. 设置开机自启
echo "⚙️ 配置开机自启..."
pm2 startup systemd -u root --hp /root
pm2 save

# 5. 显示状态
echo ""
echo "✅ 配置完成！"
echo ""
pm2 status

echo ""
echo "📚 常用命令:"
echo "  pm2 status           - 查看状态"
echo "  pm2 logs openclaw    - 查看日志"
echo "  pm2 restart openclaw - 重启服务"
echo "  pm2 stop openclaw    - 停止服务"
echo ""
echo "🦞 OpenClaw 现在后台运行，退出 SSH 也不会中断！"