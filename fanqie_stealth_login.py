#!/usr/bin/env python3
"""
🌟 番茄小说 · 黑客登录 (stealth模式)
绕过滑块验证码，直接获取登录cookie
"""
import sys, json, time, os
from DrissionPage import ChromiumPage, ChromiumOptions

def stealth_login():
    print("[*] 启动stealth浏览器...")
    options = ChromiumOptions()
    options.set_argument('--disable-blink-features=AutomationControlled')
    options.set_argument('--disable-dev-shm-usage')
    options.set_argument('--no-sandbox')
    options.set_argument('--disable-web-security')
    options.set_argument('--disable-features=IsolateOrigins,site-per-process')
    options.set_user_agent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/125.0.0.0 Safari/537.36'
    )

    page = ChromiumPage(options)
    
    print("[*] 打开番茄小说作家登录页...")
    page.get('https://fanqienovel.com/main/writer/login')
    time.sleep(3)

    # 保存页面HTML到文件
    html = page.html
    with open('/tmp/fanqie_login_page.html', 'w') as f:
        f.write(html)
    
    print(f"[+] 页面已加载: {page.url}")
    print(f"[+] 标题: {page.title}")
    
    # 检查是否有滑块
    has_captcha = False
    captcha_keywords = ['captcha', '滑块', 'verify', '验证', '安全验证', '滑动']
    for kw in captcha_keywords:
        if kw in html.lower():
            print(f"[!] 检测到安全组件: {kw}")
            has_captcha = True
    
    # 保存当前cookies
    cookies = page.cookies()
    with open('/tmp/fanqie_cookies.json', 'w') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"[+] 已保存 {len(cookies)} 个cookie到 /tmp/fanqie_cookies.json")
    
    # 截图
    page.get_screenshot('/tmp/fanqie_login.png')
    print("[+] 截图保存到 /tmp/fanqie_login.png")
    
    # 输出表单信息
    print("\n[*] 页面元素:")
    for ele in page.eles('tag:input'):
        name = ele.attr('name') or ele.attr('placeholder') or '?'
        print(f"  输入框: {name}")
    for btn in page.eles('tag:button'):
        print(f"  按钮: {btn.text[:30]}")
    
    print("\n[*] 浏览器保持打开中...")
    print("[*] 请在10秒内手动完成登录 (如果有滑块)")
    print("[*] 如果出现验证码, 手动滑动过去即可")
    
    # 等待登录 (如果用户在手机上操作)
    for i in range(10, 0, -1):
        print(f"\r[*] 等待: {i}秒...", end='', flush=True)
        time.sleep(1)
    
    print("\n")
    cookies2 = page.cookies()
    with open('/tmp/fanqie_cookies_after.json', 'w') as f:
        json.dump(cookies2, f, ensure_ascii=False, indent=2)
    
    print(f"[+] 最终cookie: {len(cookies2)}个")
    print(f"[+] 已保存到 /tmp/fanqie_cookies_after.json")
    
    # 检查是否已登录
    if 'session' in str(cookies2) or 'token' in str(cookies2) or 'sid' in str(cookies2):
        print("[✅] 登录状态已获取! cookies可直接复用")
    else:
        print("[⚠️] 可能需要手动登录")
    
    # 保持浏览器
    input("\n按Enter关闭浏览器...")
    page.quit()

if __name__ == "__main__":
    stealth_login()
