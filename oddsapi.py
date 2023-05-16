import requests
from datetime import datetime
import os
import tabulate

url = "https://api.the-odds-api.com/v3/odds"

parameters = {
    'sport': 'basketball_nba',
    'region': 'us',
    'apiKey': os.environ.get('ODDS_API_KEY')
}

response = requests.get(url, params=parameters)

data = response.json()
teams_odds = []

for game in data['data']:
    commence_time = datetime.fromtimestamp(game['commence_time']).strftime('%Y-%m-%d %H:%M')
    print(commence_time, game['teams'])
    for site in game['sites']:
        home_team = game['teams'][0]
        away_team = game['teams'][1]
        home_win_prob = site['odds']['h2h'][0]
        away_win_prob = site['odds']['h2h'][1]
        home_win_rate = round(home_win_prob / (home_win_prob + away_win_prob), 2)
        away_win_rate = round(away_win_prob / (home_win_prob + away_win_prob), 2)
    print(home_team, home_win_rate, away_team, away_win_rate)
    teams_odds.append((commence_time, game['teams'], home_team, home_win_rate, away_team, away_win_rate))

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
table = tabulate.tabulate(teams_odds, tablefmt='simple')
message = f"{table}\n"
send_to_telegram(message)