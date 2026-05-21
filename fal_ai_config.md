# fal.ai API 配置指南

## 📋 配置步骤

### 1. 注册账号
1. 访问：https://fal.ai
2. 点击 "Sign Up" 或 "Login"
3. 使用邮箱或 GitHub 账号注册

### 2. 获取 API 密钥
1. 登录后访问：https://fal.ai/dashboard/api-keys
2. 点击 "Create API Key"
3. 复制生成的密钥（格式类似：`faa1...`）

### 3. 配置到 OpenClaw

#### 方式 1: 环境变量
```bash
export FAL_KEY=your_fal_ai_api_key_here
```

#### 方式 2: 配置文件
编辑 `~/.claude.json` 或 `openclaw.json`：

```json
{
  "fal-ai": {
    "command": "npx",
    "args": ["-y", "fal-ai-mcp-server"],
    "env": {
      "FAL_KEY": "your_fal_ai_api_key_here"
    }
  }
}
```

### 4. 安装 fal-ai MCP 服务器
```bash
npm install -g fal-ai-mcp-server
```

### 5. 测试连接
```bash
npx fal-ai-mcp-server --help
```

---

## 🎯 使用示例

### 生成国风美女图片

**提示词模板**：
```
traditional Chinese beauty, guofeng style, elegant ancient Chinese dress, 
hanfu, studio lighting, soft natural light, high quality, photorealistic, 
detailed face, 8k resolution, professional photography
```

**参数配置**：
- 模型：`fal-ai/nano-banana-pro`（高质量）
- 尺寸：`square` 或 `portrait_4_3`
- 数量：1-4 张
- 引导尺度：7.5（更忠实于提示词）

---

## 💰 费用说明

- **Nano Banana 2**：约 $0.01/张（快速，适合测试）
- **Nano Banana Pro**：约 $0.05/张（高质量，适合最终输出）
- **免费额度**：新用户通常有免费试用额度

---

## 📝 提示词建议

### 国风美女提示词
```
traditional Chinese beauty, guofeng style, elegant ancient Chinese dress, 
hanfu, silk fabric, intricate embroidery, studio lighting, soft natural light, 
high quality, photorealistic, detailed face, 8k resolution, professional photography, 
chinese traditional makeup, elegant hairstyle with hairpins
```

### 不同风格
- **古典写实**：`photorealistic, studio lighting, 8k`
- **水墨画**：`ink wash painting style, traditional chinese art`
- **工笔画**：`gongbi painting, detailed line work, vibrant colors`
- **现代国风**：`modern chinese fashion, contemporary hanfu, urban background`

---

## 🔧 故障排查

### 问题 1: API 密钥无效
**解决**：检查密钥格式，确保没有空格或换行

### 问题 2: 模型加载失败
**解决**：检查网络连接，fal.ai 可能需要科学上网

### 问题 3: 生成速度慢
**解决**：使用 Nano Banana 2 而不是 Pro 版本

---

## 📞 技术支持

- **官网**：https://fal.ai
- **文档**：https://fal.ai/docs
- **Discord**：https://discord.gg/fal
- **邮箱**：support@fal.ai

---

**配置完成后，告诉我 API 密钥，我就可以为您生成国风美女图片了！** 🦞
