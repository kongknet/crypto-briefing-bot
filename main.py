import requests
import os

def get_crypto_trends():
    # 使用 CoinGecko API 抓取当前热门项目（Trending）
    # 这个 API 极度稳定，不会封禁 GitHub IP
    url = "https://api.coingecko.com/api/v3/search/trending"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        print("正在获取热门潜力项目...")
        response = requests.get(url, headers=headers, timeout=20)
        data = response.json()
        coins = data.get('coins', [])
        
        if not coins:
            return "⚠️ 今日暂无热门变动数据。"

        message = "🌟 **今日全网热门潜力项目 (Trending)**\n"
        message += "--------------------------\n"
        message += "以下项目在过去24小时内搜索热度最高，建议关注其空投交互机会：\n\n"
        
        for p in coins[:6]: # 抓取前6个
            item = p.get('item', {})
            name = item.get('name', '未知')
            symbol = item.get('symbol', 'N/A')
            rank = item.get('market_cap_rank', '未入榜')
            
            message += f"🔹 **项目:** {name} ({symbol})\n"
            message += f"📊 **市值排名:** {rank}\n"
            message += f"🔗 [点击研究](https://www.google.com/search?q={name}+crypto+airdrop+guide)\n\n"
            
        message += "--------------------------\n"
        message += "💡 技巧：Trending 列表通常是空投发币前的预热信号。"
        return message

    except Exception as e:
        print(f"抓取失败: {e}")
        return "❌ 自动化抓取暂时受阻。请检查 GitHub Actions 网络环境。"

def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"发送异常: {e}")

if __name__ == "__main__":
    content = get_crypto_trends()
    send_telegram(content)
