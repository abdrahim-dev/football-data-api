"""
API Client module for communicating with the football-data.org API.
Provides functions to fetch team data, match results, and league standings.
"""

import requests
from config import BASE_URL, HEADERS


def get_team_mapping():
    """
    Fetches all La Liga teams and creates a lookup dictionary.

    Returns:
        dict: A mapping of team ID (int) to team Name (str).
    """
    url = f"{BASE_URL}/competitions/PD/teams"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    # Using a dictionary comprehension to map IDs to Names
    return {team["id"]: team["name"] for team in data.get("teams", [])}


def get_results_fav_team(start_date, end_date, team_id):
    """
    Retrieves finished match results for a specific team within a date range.

    Args:
        start_date (str): Start date in ISO format (YYYY-MM-DD).
        end_date (str): End date in ISO format (YYYY-MM-DD).
        team_id (int): The unique ID of the team.

    Returns:
        list[dict]: A list of dictionaries containing match details and scores.
    """
    url = f"{BASE_URL}/teams/{team_id}/matches"
    params = {"dateFrom": start_date, "dateTo": end_date, "status": "FINISHED"}

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    results = []
    # Parse the raw API response into a cleaner list of match dictionaries
    for match in data.get("matches", []):
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


def get_football_teams():
    """
    Fetches metadata for all teams participating in the league.

    Returns:
        list[dict]: List containing team ID, name, short name, and TLA (abbreviation).
    """
    url = f"{BASE_URL}/competitions/PD/teams"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    return [
        {
            "id": team["id"],
            "name": team["name"],
            "short_name": team["shortName"],
            "tla": team["tla"],
        }
        for team in data.get("teams", [])
    ]


def get_league_standings():
    """
    Fetches the current league table/standings.

    Returns:
        list[dict]: List of teams with their current position and points.
    """
    url = f"{BASE_URL}/competitions/PD/standings"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    standings = []
    # The API returns multiple standing types; we iterate through the 'table'
    for standing in data.get("standings", []):
        for team in standing.get("table", []):
            standings.append(
                {
                    "position": team["position"],
                    "team_name": team["team"]["name"],
                    "points": team["points"],
                }
            )
    return standings
