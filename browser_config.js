const { chromium } = require('playwright');

async function main() {
  console.log('启动 Chrome 浏览器...');
  
  const browser = await chromium.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });
  
  const page = await browser.newPage();
  await page.goto('https://entrocamp.coze.com/agent/g751i897', {
    waitUntil: 'networkidle',
    timeout: 30000
  });
  
  console.log('页面加载完成');
  
  // 截图
  await page.screenshot({ path: '/tmp/entrocamp_learning.png', fullPage: true });
  console.log('截图保存：/tmp/entrocamp_learning.png');
  
  // 获取页面标题
  const title = await page.title();
  console.log('页面标题:', title);
  
  await browser.close();
  console.log('浏览器已关闭');
}

main().catch(console.error);
