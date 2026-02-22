import requests
import os

API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SPORT = "basketball_nba"
REGIONS = "us"
MARKETS = "player_points,player_rebounds,player_assists"
ODDS_FORMAT = "decimal"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def scan():
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT
    }

    response = requests.get(url, params=params)

    print("STATUS CODE:", response.status_code)
    print("RAW RESPONSE:", response.text)

    if response.status_code != 200:
    send_telegram(f"API ERROR ❌\nStatus: {response.status_code}\n{response.text}")
    return

    try:
        data = response.json()
    except:
        send_telegram("JSON PARSE ERROR ❌")
        return

    if not isinstance(data, list):
        send_telegram("API trả về không phải list ❌")
        return

    message = "NBA Scan Running ✅\n"

    for game in data:
        home = game.get("home_team")
        away = game.get("away_team")
        message += f"\n{away} @ {home}"

    send_telegram(message)

if __name__ == "__main__":
    scan()
