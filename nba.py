import requests
from datetime import datetime
import os
import tabulate

url = "https://api.the-odds-api.com/v4/sports/basketball_nba/scores/"

parameters = {
    'daysFrom': 1,
    'apiKey': os.environ.get('ODDS_API_KEY')
}

response = requests.get(url, params=parameters)

data = response.json()
teams_scores = []

for score in data:
    if score.get('completed'):
        home_team = score['home_team']
        away_team = score['away_team']
        home_score = score['scores'][0]['score']
        away_score = score['scores'][1]['score']
    print(f"{home_team} {home_score} - {away_team} {away_score}")
    teams_scores.append((home_team, home_score, away_team, away_score))

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
table = tabulate.tabulate(teams_scores, tablefmt='simple')
message = f"{table}"
send_to_telegram(message)