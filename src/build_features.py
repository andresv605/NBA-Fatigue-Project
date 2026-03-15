import os
import pandas as pd

IN_PATH = os.path.join("data", "processed", "team_games.csv")
OUT_PATH = os.path.join("data", "processed", "team_games_features.csv")


def main():
    if not os.path.exists(IN_PATH):
        raise FileNotFoundError(f"Missing {IN_PATH}. Run build_team_games.py first.")

    df = pd.read_csv(IN_PATH)
    df["game_date"] = pd.to_datetime(df["game_date"])

    #Sort per team
    df = df.sort_values(["team_id", "game_date", "game_id"]).reset_index(drop=True)

    #Point differential
    df["point_diff"] = df["team_pts"] - df["opp_pts"]

    #Rest days: difference between this game and previous game for same team
    df["prev_game_date"] = df.groupby("team_id")["game_date"].shift(1)
    df["rest_days"] = (df["game_date"] - df["prev_game_date"]).dt.days

    #Back-to-back checker
    df["b2b"] = df["rest_days"].apply(lambda x: 1 if x == 1 else 0)

    #Clean up
    df = df.drop(columns=["prev_game_date"])
    df["game_date"] = df["game_date"].dt.strftime("%Y-%m-%d")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Saved features -> {OUT_PATH}")
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    main()
