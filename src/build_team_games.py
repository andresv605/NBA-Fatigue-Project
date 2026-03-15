import os
import pandas as pd

RAW_PATH = os.path.join("data", "raw", "games_raw.csv")
OUT_PATH = os.path.join("data", "processed", "team_games.csv")


def main():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Missing {RAW_PATH}. Run collect_games.py first.")

    df = pd.read_csv(RAW_PATH)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    rows = []
    for _, r in df.iterrows():
        #Home team row
        rows.append({
            "game_id": r["game_id"],
            "game_date": r["game_date"],
            "team_id": r["home_team_id"],
            "team_name": r["home_team_name"],
            "opponent_id": r["away_team_id"],
            "opponent_name": r["away_team_name"],
            "home_away": "HOME",
            "team_pts": r["home_pts"],
            "opp_pts": r["away_pts"],
            "win": 1 if r["home_pts"] > r["away_pts"] else 0
        })
        #Away team row
        rows.append({
            "game_id": r["game_id"],
            "game_date": r["game_date"],
            "team_id": r["away_team_id"],
            "team_name": r["away_team_name"],
            "opponent_id": r["home_team_id"],
            "opponent_name": r["home_team_name"],
            "home_away": "AWAY",
            "team_pts": r["away_pts"],
            "opp_pts": r["home_pts"],
            "win": 1 if r["away_pts"] > r["home_pts"] else 0
        })

    out = pd.DataFrame(rows).drop_duplicates(subset=["game_id", "team_id"])
    out = out.sort_values(["team_id", "game_date", "game_id"])
    out.to_csv(OUT_PATH, index=False)

    print(f"Built team-game table: {len(out)} rows")
    print(f"Saved -> {OUT_PATH}")


if __name__ == "__main__":
    main()
