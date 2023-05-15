import requests
import os


def send_to_telegram(message):
    apiToken = os.environ.get('TELEGRAM_API_TOKEN')
    chatID = os.environ.get('TELEGRAM_CHAT_ID')
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(
            apiURL, data={'chat_id': chatID, 'text': message, 'parse_mode': 'Markdown'})
        print(response.text)
    except Exception as e:
        print(e)


# 發送消息至telegram
url = 'https://www.sportslottery.com.tw/zh-tw/news/live-schedule'
message = f"{url}\n"
send_to_telegram(message)
