import requests
import pandas as pd
from pathlib import Path


def fetch_fixtures_espn(season_start=2025):

    start = f"{season_start}0701"
    end = f"{season_start + 1}0630"
    url = (
        "https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard"
    )
    params = {"dates": f"{start}-{end}", "limit": 1000}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    events = payload.get("events") or []
    rows = []
    for event in events:
        competition = (event.get("competitions") or [{}])[0]
        competitors = competition.get("competitors") or []

        home = next((c for c in competitors if c.get("homeAway") == "home"), {})
        away = next((c for c in competitors if c.get("homeAway") == "away"), {})

        home_score = home.get("score")
        away_score = away.get("score")
        rows.append(
            {
                "date": (event.get("date") or "").split("T")[0],
                "home_team": (home.get("team") or {}).get("displayName"),
                "away_team": (away.get("team") or {}).get("displayName"),
                "home_goals": int(home_score) if str(home_score).isdigit() else None,
                "away_goals": int(away_score) if str(away_score).isdigit() else None,
                "stadium": (competition.get("venue") or {}).get("fullName"),
            }
        )

    return pd.DataFrame(rows)


def main():
    try:
        df = fetch_fixtures_espn(season_start=2025)
    except Exception as exc:
        print(f"Failed to fetch data: {exc}")
        return

    if df.empty:
        print("No data returned from API.")
        return

    output_file = Path(__file__).with_name("champions_league_matches.csv")
    df.to_csv(output_file, index=False)
    print(f"Dataset saved to {output_file} from ESPN API.")

if __name__ == "__main__":
    main()