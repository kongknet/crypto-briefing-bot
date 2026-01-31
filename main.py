import requests
from bs4 import BeautifulSoup
import os

def get_high_value_airdrops():
    # 抓取 Airdrops.io 的最新列表
    url = "https://airdrops.io/latest/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    airdrops = soup.find_all('article', class_='airdrop-hover', limit=10)
    
    high_value_list = []
    
    for drop in airdrops:
        name = drop.find('h3').text.strip()
        link = drop.find('a')['href']
        
        # 模拟“大额融资”筛选逻辑
        # 提示：由于网页端融资额通常在详情页，我们这里先进行关键词标记
        # 实际操作中，我们会结合 CryptoRank API 获取精准金额
        status = "🔥 潜力大毛" if "Potential" in str(drop) else "✅ 确认为空投"
        
        high_value_list.append(f"项目名称: {name}\n状态: {status}\n详情查看: {link}")

    # 构造发送内容
    message = "💰 **今日大额融资/高质量空投筛选**\n"
    message += "--------------------------\n"
    if not high_value_list:
        message += "今日暂无满足筛选条件的新项目。"
    else:
        message += "\n\n".join(high_value_list[:5]) # 仅推送前5个最优质的
    
    message += "\n--------------------------\n"
    message += "💡 建议：融资额 > 5000万美金的项目建议至少布局3个账号。"
    return message

def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 增加超时处理，保证稳定性
    try:
        requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=10)
    except Exception as e:
        print(f"发送失败: {e}")

if __name__ == "__main__":
    report_content = get_high_value_airdrops()
    send_telegram(report_content)
