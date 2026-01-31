import requests
import os
import google.generativeai as genai
import xml.etree.ElementTree as ET

def get_x_expert_updates(screen_name):
    # 使用公开的 RSSHub 实例监听 X 账号 (无需 API Key)
    rss_url = f"https://rsshub.app/twitter/user/{screen_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(rss_url, headers=headers, timeout=20)
        root = ET.fromstring(response.content)
        updates = []
        
        # 抓取最新的 3 条推文内容
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text
            description = item.find('description').text
            updates.append(f"推文内容: {title}\n详情: {description}")
        
        return "\n".join(updates)
    except Exception as e:
        print(f"X 抓取失败: {e}")
        return "无法获取推文动态"

def get_ai_analysis(market_data, x_data):
    # 配置 Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # 使用最新的 flash 模型速度更快
    
    prompt = f"""
    你是一个顶级加密货币分析师。请结合以下两部分信息生成简报：
    
    1. 【今日融资/热门数据】：
    {market_data}
    
    2. 【KOL @Benjieming1Q84 的最新动态】：
    {x_data}
    
    要求：
    - 总结本杰明最近在关注什么、推荐什么操作。
    - 结合融资数据，给出 2-3 个优先级最高的空投任务建议。
    - 使用简洁的中文，分条罗列。
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 总结失败: {str(e)}"

# ... (保留你之前的 get_crypto_trends 函数) ...

if __name__ == "__main__":
    # 1. 抓取市场趋势
    market_info = get_crypto_trends()
    # 2. 抓取本杰明的推文
    x_expert_info = get_x_expert_updates("Benjieming1Q84")
    # 3. 让 AI 进行综合研判
    final_briefing = get_ai_analysis(market_info, x_expert_info)
    # 4. 发送到 Telegram
    send_telegram(f"🛡️ **Gemini 深度情报 (含本杰明动态)**\n\n{final_briefing}")
