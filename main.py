import requests
from bs4 import BeautifulSoup
import os

def get_latest_airdrops():
    url = "https://airdrops.io/latest/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 抓取前 5 个最新的空投项目
    airdrops = soup.find_all('article', class_='airdrop-hover', limit=5)
    
    content = "🚀 **今日全网最新空投情报**\n\n"
    for drop in airdrops:
        name = drop.find('h3').text.strip()
        link = drop.find('a')['href']
        content += f"🔹 **项目:** {name}\n🔗 **详情:** {link}\n\n"
    
    content += "---\n🤖 *信息抓取自 Airdrops.io*"
    return content

def send_telegram(text):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

if __name__ == "__main__":
    report = get_latest_airdrops()
    send_telegram(report)
