import requests
import os
from datetime import datetime

def send_to_telegram(message):
    # 使用os.environ获取Github仓库的secrets
    apiToken = os.environ.get('TELEGRAM_API_TOKEN')
    chatID = os.environ.get('TELEGRAM_CHAT_ID')
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, data={'chat_id': chatID, 'text': message, 'parse_mode': 'Markdown'})
        print(response.text)
    except Exception as e:
        print(e)


def send_to_gfuns(name_param):
    apiURL = "https://functions-mlb-5lezkyhrzq-de.a.run.app"
    try:
        response = requests.get(apiURL, params={'name': name_param})
        print(response.text)
    except Exception as e:
        print(e)

def query_from_gfuns():
    today = '20230610' # datetime.today().strftime('%Y%m%d')
    apiURL = "https://functions-mlb-query-5lezkyhrzq-de.a.run.app"
    try:
        response = requests.get(apiURL, params={'day': today})
        print(response.text)
        return response["MLB"]
    except Exception as e:
        print(e)