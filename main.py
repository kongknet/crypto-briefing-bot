import requests
import os
import google.generativeai as genai
import xml.etree.ElementTree as ET

# 1. 获取市场趋势数据 (CoinGecko)
def get_crypto_trends():
    url = "https://api.coingecko.com/api/v3/search/trending"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        data = response.json()
        coins = data.get('coins', [])
        summary = ""
        for p in coins[:5]:
            item = p.get('item', {})
            summary += f"项目: {item.get('name')} ({item.get('symbol')}), 市值排名: {item.get('market_cap_rank')}\n"
        return summary
    except Exception as e:
        return f"无法获取实时趋势数据: {e}"

# 2. 获取本杰明 X 动态 (RSSHub)
def get_x_expert_updates(screen_name):
    # 如果 rsshub.app 响应慢，可以尝试换成别的实例
    rss_url = f"https://rsshub.app/twitter/user/{screen_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(rss_url, headers=headers, timeout=25)
        root = ET.fromstring(response.content)
        updates = []
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text
            updates.append(f"- {title}")
        return "\n".join(updates)
    except Exception as e:
        return f"暂时无法获取 X 专家动态"

# 3. Gemini AI 深度总结
def get_ai_analysis(market_data, x_data):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "错误: 未配置 GEMINI_API_KEY"
    
    genai.configure(api_key=api_key)
    # 使用推荐的 gemini-1.5-flash，速度快且免费额度足
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    你是一个顶级加密货币分析师。请结合以下信息生成一份中文简报：
    
    【今日热门趋势项目】：
    {market_data}
    
    【KOL @Benjieming1Q84 最新动态】：
    {x_data}
    
    请重点评价这些项目的空投潜力，并给出具体的交互建议。
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 总结生成失败: {e}"

# 4. 发送 Telegram
def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": text,
        "disable_web_page_preview": "true"
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    # 执行流程
    print("开始获取数据...")
    market_info = get_crypto_trends()
    x_info = get_x_expert_updates("Benjieming1Q84")
    
    print("正在调用 Gemini AI 分析...")
    final_briefing = get_ai_analysis(market_info, x_info)
    
    print("发送简报到 Telegram...")
    header = "🛡️ **Gemini AI 专家点评版简报**\n\n"
    send_telegram(header + final_briefing)
