import requests
import os

API_KEY = os.environ.get("API_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

EV_THRESHOLD = 0.03

def send_alert(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def remove_vig(over, under):
    p_over = 1/over
    p_under = 1/under
    total = p_over + p_under
    return p_over/total

def calculate_ev(true_p, soft_odds):
    return (true_p * soft_odds) - 1

def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "player_points,player_assists,player_rebounds",
        "bookmakers": "fanduel,stake"
    }
    return requests.get(url, params=params).json()

def scan():
    data = get_odds()

    for game in data:
        bookmakers = {b["key"]: b for b in game.get("bookmakers", [])}

        if "fanduel" not in bookmakers or "stake" not in bookmakers:
            continue

        sharp = bookmakers["fanduel"]
        soft = bookmakers["stake"]

        # Demo logic (ta sẽ nâng cấp mapping sau)
        sharp_over = 1.85
        sharp_under = 1.95
        soft_over = 2.05

        true_p = remove_vig(sharp_over, sharp_under)
        ev = calculate_ev(true_p, soft_over)

        if ev > EV_THRESHOLD:
            send_alert(f"VALUE FOUND! EV={round(ev*100,2)}%")

scan()
