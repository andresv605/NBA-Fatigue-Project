import os
import sys
from datetime import datetime, timedelta
from wsgiref import headers
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BALLDONTLIE_API_KEY", "").strip()
BASE_URL = os.getenv("BALLDONTLIE_BASE_URL", "https://api.balldontlie.io/v1").strip()

RAW_PATH = os.path.join("data", "raw", "games_raw.csv")


def get_target_date() -> str:
    # Allow date override: python src/collect_games.py 2026-02-01
    if len(sys.argv) >= 2:
        return sys.argv[1]
    # Default: yesterday
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def fetch_games_for_date(date_str: str) -> list[dict]:
    """
    Fetch games for a date. Endpoint shape may vary slightly by API version.
    Adjust params if needed based on your account/docs.
    """
    url = f"{BASE_URL}/games"
    headers = {}
    if API_KEY:
        headers["Authorization"] = API_KEY


    params = {
        "dates[]": date_str,
        "per_page": 100
    }

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Typical format: {"data":[...], "meta":{...}}
    return data.get("data", [])


def normalize_games(games: list[dict], date_str: str) -> pd.DataFrame:
    rows = []
    for g in games:
        # Defensive parsing (field names can differ slightly)
        game_id = g.get("id")
        home = g.get("home_team", {}) or {}
        away = g.get("visitor_team", {}) or g.get("away_team", {}) or {}

        home_pts = g.get("home_team_score")
        away_pts = g.get("visitor_team_score") if "visitor_team_score" in g else g.get("away_team_score")

        # Only keep completed games with scores
        if game_id is None or home_pts is None or away_pts is None:
            continue

        rows.append({
            "game_id": int(game_id),
            "game_date": date_str,
            "home_team_id": home.get("id"),
            "home_team_name": home.get("full_name") or home.get("name"),
            "away_team_id": away.get("id"),
            "away_team_name": away.get("full_name") or away.get("name"),
            "home_pts": int(home_pts),
            "away_pts": int(away_pts),
        })

    return pd.DataFrame(rows)


def append_dedup(df_new: pd.DataFrame, path: str) -> pd.DataFrame:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if os.path.exists(path):
        df_old = pd.read_csv(path)
        # Combine then drop duplicate game_id
        df_all = pd.concat([df_old, df_new], ignore_index=True)
        df_all = df_all.drop_duplicates(subset=["game_id"]).sort_values(["game_date", "game_id"])
    else:
        df_all = df_new.sort_values(["game_date", "game_id"])

    df_all.to_csv(path, index=False)
    return df_all


def main():
    date_str = get_target_date()
    print(f"Collecting games for date: {date_str}")

    games = fetch_games_for_date(date_str)
    df_new = normalize_games(games, date_str)

    if df_new.empty:
        print("No completed games found (or API returned none).")
        return

    df_all = append_dedup(df_new, RAW_PATH)
    print(f"Added {len(df_new)} rows. Total games stored: {len(df_all)}")
    print(f"Saved -> {RAW_PATH}")


if __name__ == "__main__":
    main()
