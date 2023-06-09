import requests
from datetime import datetime
import os
import tabulate
import helper
import mlb_team

url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/scores/"
params = {
    'daysFrom': 1,
    'apiKey': os.environ.get('ODDS_API_KEY')
}

response = requests.get(url, params=params)
data = response.json()

teams_scores = []
dominant_team = []

for score in data:
    if score.get('completed'):
        home_team = score['home_team']
        away_team = score['away_team']
        home_score = int(score['scores'][0]['score'])
        away_score = int(score['scores'][1]['score'])
        datetime_obj = datetime.strptime(score['commence_time'], '%Y-%m-%dT%H:%M:%SZ')
        commence_time = datetime_obj.strftime('%Y-%m-%d %H:%M')
    
        # 判断获胜队伍
        if home_score > away_score:
            winning_team = home_team
        elif away_score > home_score:
            winning_team = away_team
        else:
            winning_team = "Tie"
        team_abbr = mlb_team.team_abbreviations.get(winning_team)
        team_abbr_zh = mlb_team.team_abbreviations_zh.get(winning_team)
        print(f"{commence_time} {home_team} {home_score} - {away_team} {away_score} (Winner: {winning_team})")
        home_vs_away = f"{home_team} {home_score} vs. {away_team} {away_score}"
        teams_scores.append((commence_time, home_vs_away))
        teams_scores.append((team_abbr, team_abbr_zh, winning_team))

        dominant_team.append(team_abbr)

url = "https://api.the-odds-api.com/v3/odds"

sport_key = "baseball_mlb"
region = "us" # uk | us | eu | au
mkt = "h2h" # h2h | spreads | totals

response = requests.get(url, params={
    "api_key": os.environ.get('ODDS_API_KEY'),
    "sport": sport_key,
    "region": region,
    "mkt": mkt
})

winners_list = []
odd_strong_team = helper.query_from_gfuns()
if odd_strong_team:
    mlb_data = odd_strong_team['MLB']
    print(mlb_data)
    dominant_set = set(dominant_team)
    mlb_set = set(mlb_data)
    # 取得相同的值
    common_values = dominant_set.intersection(mlb_set)

    # 將結果轉換為陣列
    winners_list = list(common_values)

# 發送消息至telegram
dominant_team_count = len(dominant_team)
table = tabulate.tabulate(teams_scores, tablefmt='simple')
message = f"{table}\n{dominant_team}\n{dominant_team_count}\n{winners_list}"
helper.send_to_telegram(message)