import requests
import os

def get_crypto_raises():
    # 优先尝试 DefiLlama API
    url = "https://api.llama.fi/raises"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print("正在从 DefiLlama 获取数据...")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status() # 如果返回 403 或 500 会报错
        data = response.json()
        raises = data.get('raises', [])
        
        if not raises:
            return "⚠️ 今日暂无公开的融资变动。"

        message = "🚀 **今日大额融资 & 潜力空投项目**\n"
        message += "--------------------------\n"
        
        count = 0
        for p in raises[:12]:
            amount = p.get('amount', 0)
            name = p.get('name', '未知项目')
            sector = p.get('sector', '其它')
            lead = p.get('leadInvestors', ['未披露'])[0]
            
            # 筛选：融资 > $5M 或 未披露的大项目
            if amount >= 5 or amount == 0:
                amt_str = f"${amount}M" if amount > 0 else "金额未披露"
                message += f"🔹 **项目:** {name}\n"
                message += f"💰 **金额:** {amt_str} | **赛道:** {sector}\n"
                message += f"👤 **领投:** {lead}\n"
                message += f"🔗 [点击搜索](https://www.google.com/search?q={name}+crypto+airdrop)\n\n"
                count += 1
            if count >= 5: break
            
        return message

    except Exception as e:
        print(f"DefiLlama 抓取失败: {e}")
        # 备选方案：如果 API 挂了，发送一个基础预警
        return "❌ 自动化抓取暂时受阻。建议手动查看：https://cryptorank.io/funding-rounds"

def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 修正：如果内容过长或格式有误，Telegram 会报 Bad Request
    # 使用 MarkdownV2 比较严格，这里改用更稳健的 HTML 格式
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        if not res.json().get("ok"):
            print(f"Telegram 发送失败: {res.text}")
    except Exception as e:
        print(f"网络异常: {e}")

if __name__ == "__main__":
    content = get_crypto_raises()
    send_telegram(content)
