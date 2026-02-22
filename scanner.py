import requests
import os

API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

def main():
    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        error_message = f"API ERROR ❌\nStatus Code: {response.status_code}\nResponse:\n{response.text}"
        send_telegram(error_message)
        return

    data = response.json()

    if not data:
        send_telegram("No NBA games found today.")
        return

    message = "NBA Games Today 🏀\n\n"

    for game in data:
        home = game["home_team"]
        away = game["away_team"]
        message += f"{away} vs {home}\n"

    send_telegram(message)

if __name__ == "__main__":
    main()
