"""
football_advanced_api_v1.1

This script fetches, processes, and visualizes football data from the
football-data.org API.

Main features:
- Fetch match results for a selected La Liga team within a date range
- Compute wins, draws, losses, and matches played for the selected team
- Export match results, team lists, league standings, and statistics to CSV and JSON
- Visualize team statistics using a pie chart

Design notes:
- No global data containers: all data flows through function parameters and return values
- Team statistics are computed using a "goals for vs goals against" approach
- Functions are kept small and focused (single responsibility)
- Code is organized into sections with clear headers and comments
- Uses environment variables (.env) for API configuration
"""

import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# -------------------------------------------------------------------
# API configuration
# -------------------------------------------------------------------

load_dotenv()
BASE_URL = os.getenv("DATABASE_URL")
headers = {"X-Auth-Token": os.getenv("API_KEY")}

# -------------------------------------------------------------------
# User input
# -------------------------------------------------------------------

fav_team = input(
    """\nEnter your favorite team ID from the list below:

ID    NAME                       SHORT_NAME       TLA
77    Athletic Club              Athletic         ATH
78    Club Atlético de Madrid    Atleti           ATL
79    CA Osasuna                 Osasuna          OSA
80    RCD Espanyol de Barcelona  Espanyol         ESP
81    FC Barcelona               Barça            FCB
82    Getafe CF                  Getafe           GET
86    Real Madrid CF             Real Madrid      RMA
87    Rayo Vallecano de Madrid   Rayo Vallecano   RAY
88    Levante UD                 Levante          LEV
89    RCD Mallorca               Mallorca         MAL
90    Real Betis Balompié        Real Betis       BET
92    Real Sociedad de Fútbol    Real Sociedad    RSO
94    Villarreal CF              Villarreal       VIL
95    Valencia CF                Valencia         VAL
263   Deportivo Alavés           Alavés           ALA
285   Elche CF                   Elche            ELC
298   Girona FC                  Girona           GIR
558   RC Celta de Vigo           Celta            CEL
559   Sevilla FC                 Sevilla FC       SEV
1048  Real Oviedo                Real Oviedo      OVI

Your favorite team ID:
"""
)

print(f"\nYou selected team code: {fav_team}")


# -------------------------------------------------------------------
# Helper / API functions
# -------------------------------------------------------------------


def get_team_mapping():
    """
    Fetch all La Liga teams and return a mapping of team_id -> team_name.

    Returns:
        dict[int, str]: Dictionary mapping team IDs to team names
    """
    url = f"{BASE_URL}/competitions/PD/teams"
    response = requests.get(url, headers=headers)
    data = response.json()

    team_map = {}

    for team in data.get("teams", []):
        team_map[team["id"]] = team["name"]

    return team_map


def get_date_range():
    """
    Ask the user for a start and end date and validate the input format.

    Returns:
        tuple[str, str]: (start_date, end_date) in ISO format (YYYY-MM-DD)
    """
    try:
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        return start_date.isoformat(), end_date.isoformat()

    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        exit(1)


def get_results_fav_team(start_date, end_date, team_id):
    """
    Fetch finished matches for a specific team within a date range.

    Args:
        start_date (str): Start date in ISO format
        end_date (str): End date in ISO format
        team_id (int): Team ID to fetch matches for

    Returns:
        list[dict]: List of match result dictionaries
    """
    results = []

    url = f"{BASE_URL}/teams/{team_id}/matches"
    params = {
        "dateFrom": start_date,
        "dateTo": end_date,
        "status": "FINISHED",
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    matches = data.get("matches", [])

    for match in matches:
        results.append(
            {
                "date": match["utcDate"],
                "home_team_id": match["homeTeam"]["id"],
                "away_team_id": match["awayTeam"]["id"],
                "home_team_name": match["homeTeam"]["name"],
                "away_team_name": match["awayTeam"]["name"],
                "home_score": match["score"]["fullTime"]["home"],
                "away_score": match["score"]["fullTime"]["away"],
            }
        )

    return results


def compute_team_stats(results, team_id):
    """
    Compute wins, draws, losses, and matches played for a given team.

    The logic is based on goals scored vs goals conceded, independent
    of home or away status.

    Args:
        results (list[dict]): Match results
        team_id (int): Team ID to compute statistics for

    Returns:
        dict: Dictionary containing wins, draws, losses, matches_played
    """
    stats = {
        "wins": 0,
        "draws": 0,
        "losses": 0,
    }

    for match in results:
        if team_id == match["home_team_id"]:
            goals_for = match["home_score"]
            goals_against = match["away_score"]

        elif team_id == match["away_team_id"]:
            goals_for = match["away_score"]
            goals_against = match["home_score"]

        else:
            continue

        if goals_for > goals_against:
            stats["wins"] += 1
        elif goals_for < goals_against:
            stats["losses"] += 1
        else:
            stats["draws"] += 1

    stats["matches_played"] = stats["wins"] + stats["draws"] + stats["losses"]

    return stats


def get_football_teams():
    """
    Fetch all teams participating in La Liga.

    Returns:
        list[dict]: List of team metadata
    """
    teams_list = []

    url = f"{BASE_URL}/competitions/PD/teams"
    response = requests.get(url, headers=headers)
    data = response.json()
    teams = data.get("teams", [])

    for team in teams:
        teams_list.append(
            {
                "id": team["id"],
                "name": team["name"],
                "short_name": team["shortName"],
                "tla": team["tla"],
            }
        )

    return teams_list


def get_league_standings():
    """
    Fetch the current La Liga standings.

    Returns:
        list[dict]: League table with positions and points
    """
    standings = []

    url = f"{BASE_URL}/competitions/PD/standings"
    response = requests.get(url, headers=headers)
    data = response.json()
    standings_list = data.get("standings", [])

    for standing in standings_list:
        # 'table' is a list of teams
        for team in standing.get("table", []):
            standings.append(
                {
                    "position": team["position"],
                    "team_name": team["team"]["name"],
                    "points": team["points"],
                    # "playedGames": team.get("playedGames", 0),
                    # "won": team.get("won", 0),
                    # "draw": team.get("draw", 0),
                    # "lost": team.get("lost", 0)
                }
            )

    return standings


def data_to_dataframe(data, filename):
    """
    Convert data to a pandas DataFrame and export it to CSV and JSON.

    Args:
        data (list[dict]): Data to export
        filename (str): Base filename (without extension)

    Returns:
        pandas.DataFrame
    """
    df = pd.DataFrame(data)
    print(df)
    df.to_csv(f"output/{filename}.csv", index=False)
    df.to_json(f"output/{filename}.json", orient="records", indent=2)
    return df


def plot_team_stats_pie(stats):
    """
    Plot and save a pie chart visualizing wins, draws, and losses.

    Args:
        stats (dict): Team statistics dictionary
    """
    labels = ["Wins", "Draws", "Losses"]
    values = [stats["wins"], stats["draws"], stats["losses"]]
    colors = ["#22D428", "#FFBF00", "#FB3333"]

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.title(f"Results Distribution for {stats['team_name']}")
    plt.axis("equal")  # makes the pie a circle
    plt.legend(labels, loc="upper right")
    plt.savefig(f"output/{team_name}_stats_pie_chart.png")

    plt.tight_layout()
    plt.show()


# -------------------------------------------------------------------
# Main execution
# -------------------------------------------------------------------


if __name__ == "__main__":
    start_date_user, end_date_user = get_date_range()
    team_id = int(fav_team)
    results = get_results_fav_team(start_date_user, end_date_user, team_id)
    data_to_dataframe(results, "results_of_matches")
    print(
        "\nThe results were saved to 'output/results_of_matches.csv' and 'output/results_of_matches.json'\n"
    )

    team_map = get_team_mapping()
    team_id = int(fav_team)
    team_name = team_map.get(team_id, "Unknown Team")

    stats = compute_team_stats(results, team_id)
    stats["team_id"] = team_id
    stats["team_name"] = team_name

    pd.DataFrame([stats]).to_csv(f"output/{team_name}_statistics.csv", index=False)
    pd.DataFrame([stats]).to_json(
        f"output/{team_name}_statistics.json", orient="records", indent=2
    )
    print(
        f"\nThe statistics of your favorite team were saved to 'output/{team_name}_statistics.csv' and 'output/{team_name}_statistics.json'\n"
    )
    plot_team_stats_pie(stats)

    football_teams = get_football_teams()
    data_to_dataframe(football_teams, "football_teams")
    print(
        "\nData saved to 'output/football_teams.csv' and 'output/football_teams.json'\n"
    )

    league_standing = get_league_standings()
    data_to_dataframe(league_standing, "league_standing")
    print(
        "\nData saved to 'output/league_standing.csv' and 'output/league_standing.json'\n"
    )
