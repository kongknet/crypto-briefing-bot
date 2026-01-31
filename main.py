import requests
import os
from datetime import datetime

def get_latest_fundraising():
    # 使用 DefiLlama 的融资 API，数据极其稳定且权威
    url = "https://api.llama.fi/raises"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        raises = data.get('raises', [])
        
        # 筛选逻辑：融资额大于 1000 万美金的项目 (或者显示为 Unknown 的潜力股)
        # 我们只看最近 7 天内公布的项目
        content = "🚀 **今日大额融资 & 潜力空投项目**\n"
        content += "--------------------------\n"
        
        count = 0
        for project in raises[:15]: # 扫描最近的15个项目
            amount = project.get('amount', 0)
            name = project.get('name', 'Unknown')
            sector = project.get('sector', 'Infrastructure')
            lead_investor = project.get('leadInvestors', ['N/A'])[0]
            
            # 筛选条件：融资额 > 10M 或者融资额为 0 (通常是未披露大额项目)
            if amount == 0 or amount >= 10:
                amount_str = f"${amount}M" if amount > 0 else "未披露"
                content += f"🔹 **项目:** {name}\n"
                content += f"💰 **金额:** {amount_str} | **赛道:** {sector}\n"
                content += f"👤 **领投方:** {lead_investor}\n"
                content += f"🔗 [点击研究](https://www.google.com/search?q={name}+crypto+airdrop)\n\n"
                count += 1
            
            if count >= 5: break # 每天推送最精华的5个项目

        if count == 0:
            content += "今日暂无大额融资变动。"
            
        content += "--------------------------\n"
        content += "🤖 数据源: DefiLlama Real-time Raises"
        return content
        
    except Exception as e:
        return f"❌ 抓取失败: {str(e)}"

def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text, "disable_web_page_preview": "true"})

if __name__ == "__main__":
    report = get_latest_fundraising()
    send_telegram(report)
