# Playwright 配置 - 使用系统 Chrome

## 配置说明

Playwright 默认使用内置 Chromium，但我们可以配置使用系统 Chrome。

## 环境变量配置

```bash
export PLAYWRIGHT_BROWSERS_PATH=/usr/bin/google-chrome
export CHROME_PATH=/usr/bin/google-chrome
```

## 验证配置

```bash
google-chrome --version
# 输出：Google Chrome 148.0.7778.96
```

## 使用方式

### 方式 1: 直接在代码中指定
```javascript
const { chromium } = require('playwright');
const browser = await chromium.launch({
  executablePath: '/usr/bin/google-chrome'
});
```

### 方式 2: 使用系统 Chrome 启动
```bash
google-chrome --headless --disable-gpu --no-sandbox --screenshot=/tmp/test.png https://example.com
```

## 当前状态

✅ Chrome 已安装：/usr/bin/google-chrome
✅ 版本：148.0.7778.96
✅ 可运行：是

## 下一步

可以直接使用系统 Chrome 进行浏览器自动化任务。
