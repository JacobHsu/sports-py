import requests
from datetime import datetime
import os
import tabulate
import helper

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

team_abbreviations = {
    'Arizona Diamondbacks': 'ARI',
    'Atlanta Braves': 'ATL',
    'Baltimore Orioles': 'BAL',
    'Boston Red Sox': 'BOS',
    'Chicago Cubs': 'CHC',
    'Chicago White Sox': 'CHW',
    'Cincinnati Reds': 'CIN',
    'Cleveland Guardians': 'CLE',
    'Colorado Rockies': 'COL',
    'Detroit Tigers': 'DET',
    'Houston Astros': 'HOU',
    'Kansas City Royals': 'KC',
    'Los Angeles Angels': 'LAA',
    'Los Angeles Dodgers': 'LAD',
    'Miami Marlins': 'MIA',
    'Milwaukee Brewers': 'MIL',
    'Minnesota Twins': 'MIN',
    'New York Yankees': 'NYY',
    'New York Mets': 'NYM',
    'Oakland Athletics': 'OAK',
    'Philadelphia Phillies': 'PHI',
    'Pittsburgh Pirates': 'PIT',
    'San Diego Padres': 'SD',
    'San Francisco Giants': 'SF',
    'Seattle Mariners': 'SEA',
    'St. Louis Cardinals': 'STL',
    'Tampa Bay Rays': 'TB',
    'Texas Rangers': 'TEX',
    'Toronto Blue Jays': 'TOR',
    'Washington Nationals': 'WSH'
}

teams_odds = []

if response.status_code == 200:
    data = response.json()
    for game in data["data"]:
        commence_time = datetime.fromtimestamp(game['commence_time']).strftime('%Y-%m-%d %H:%M')
        # print(commence_time, game["teams"], game["sites"][0]["odds"]["h2h"])
        teams = game["teams"]
        odds = game["sites"][0]["odds"]["h2h"]
        min_odds_index = odds.index(min(odds))
        min_odds_team = teams[min_odds_index]
        team = f"{teams[0]} vs {teams[1]}"
        team_odds = f"{odds[0]} vs {odds[1]}"
        team_abbr = team_abbreviations.get(min_odds_team)
        print(f"{commence_time} {teams[0]} vs {teams[1]} {odds} {team_abbreviations.get(min_odds_team)}: {min_odds_team} ")
        teams_odds.append((commence_time, team))
        teams_odds.append((team_odds, team_abbr, min_odds_team))
        # print(f"Team with lower odds: {min_odds_team} ")
else:
    print("Error:", response.status_code, response.text)

# 發送消息至telegram
table = tabulate.tabulate(teams_odds, tablefmt='simple')
message = f"{table}"
helper.send_to_telegram(message)