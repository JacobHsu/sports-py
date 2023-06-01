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


with open("strong_teams.txt", "r") as file:
    strong_teams_content = file.read()

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
        teams_scores.append((commence_time, home_team, home_score, 'vs.', away_team, away_score))
        teams_scores.append(((team_abbr, team_abbr_zh, winning_team))
      
    if team_abbr in strong_teams_content:
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

# 發送消息至telegram
dominant_team_count = len(dominant_team)
table = tabulate.tabulate(teams_scores, tablefmt='simple')
message = f"{table}\n{dominant_team}\n{dominant_team_count}"
helper.send_to_telegram(message)