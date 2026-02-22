"""
Football Analytics Pro API
==========================
A FastAPI-based web service providing fuzzy team searching and
Head-to-Head (H2H) match analysis using the football-data.org API.
Features:
- Fuzzy Search: Find team IDs by partial or misspelled names.
- H2H Comparison: Compare two teams' historical performance against each other.
- Interactive API Docs: Explore endpoints via Swagger UI at /docs.

"""

import os
import difflib
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# --- Configuration & Environment Setup ---
load_dotenv()

# Initialize FastAPI with metadata for the /docs (Swagger) interface
app = FastAPI(
    title="Football Analytics Pro API",
    description="Professional Football Data API with Fuzzy Search & H2H Comparison",
    version="2.0.0",
)

# API Configuration from environment variables
BASE_URL = os.getenv("DATABASE_URL", "https://api.football-data.org/v4")
API_KEY = os.getenv("API_KEY")
HEADERS = {"X-Auth-Token": API_KEY}

# --- Internal Helper Functions ---


def fetch_all_teams():
    """
    Retrieves the complete list of teams for the current league (La Liga/PD).

    Returns:
        list: A list of team dictionaries from the API.
    """
    url = f"{BASE_URL}/competitions/PD/teams"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("teams", [])


def find_team_by_name(query: str):
    """
    Uses fuzzy string matching to find a team ID based on a partial or misspelled name.
    Example: 'Barca' -> 'FC Barcelona'

    Args:
        query (str): The search string provided by the user.

    Returns:
        dict: A dictionary containing 'id' and 'name' of the best match, or None.
    """
    teams = fetch_all_teams()
    # Create a lookup dictionary mapping team names to their IDs
    team_names = {t["name"]: t["id"] for t in teams}

    # difflib finds the closest string match from the keys (team names)
    # cutoff=0.3 allows for a relatively loose/forgiving match
    matches = difflib.get_close_matches(query, team_names.keys(), n=1, cutoff=0.3)

    if not matches:
        return None

    best_match = matches[0]
    return {"id": team_names[best_match], "name": best_match}


# --- API Endpoints ---


@app.get("/", tags=["General"])
def root():
    """Welcome endpoint providing instructions for the interactive documentation."""
    return {
        "message": "Welcome to the Football Analytics API. Go to /docs for the interactive UI."
    }


@app.get("/search", tags=["Teams"])
def search_team(name: str):
    """
    Endpoint to find a team's official ID and Name using fuzzy search.

    Query Params:
        name (str): The name (or partial name) of the team.
    """
    result = find_team_by_name(name)
    if not result:
        raise HTTPException(
            status_code=404, detail="Team not found. Try a different spelling."
        )
    return result


@app.get("/compare", tags=["Analysis"])
def head_to_head(team1: str, team2: str):
    """
    Performs a Head-to-Head (H2H) comparison between two teams.
    Calculates total wins for both, draws, and provides historical match results.

    Args:
        team1 (str): Name of the first team.
        team2 (str): Name of the second team.
    """
    # 1. Resolve team names to IDs using our fuzzy search helper
    team_1 = find_team_by_name(team1)
    team_2 = find_team_by_name(team2)

    if not team_1 or not team_2:
        raise HTTPException(status_code=404, detail="One or both teams not found.")

    # 2. Fetch match history for the first team
    url = f"{BASE_URL}/teams/{team_1['id']}/matches"
    response = requests.get(url, headers=HEADERS, params={"status": "FINISHED"})
    all_matches = response.json().get("matches", [])

    # 3. Filter matches where the opponent was the second team
    h2h_matches = [
        m
        for m in all_matches
        if (m["homeTeam"]["id"] == team_2["id"] or m["awayTeam"]["id"] == team_2["id"])
    ]

    # 4. Initialize counters for statistics
    team1_wins = 0
    team2_wins = 0
    draws = 0

    # 5. Calculate H2H performance
    for m in h2h_matches:
        home_score = m["score"]["fullTime"]["home"]
        away_score = m["score"]["fullTime"]["away"]

        if home_score == away_score:
            draws += 1
        # Check if Team 1 won as Home team or Away team
        elif (m["homeTeam"]["id"] == team_1["id"] and home_score > away_score) or (
            m["awayTeam"]["id"] == team_1["id"] and away_score > home_score
        ):
            team1_wins += 1
        else:
            team2_wins += 1

    # Return structured JSON response
    return {
        "comparison": f"{team_1['name']} vs {team_2['name']}",
        "stats": {
            f"{team_1['name']}_wins": team1_wins,
            f"{team_2['name']}_wins": team2_wins,
            "draws": draws,
            "total_matches": len(h2h_matches),
        },
        "history": [
            {
                "date": m["utcDate"],
                "score": f"{m['homeTeam']['name']} {m['score']['fullTime']['home']} - {m['score']['fullTime']['away']} {m['awayTeam']['name']}",
            }
            for m in h2h_matches
        ],
    }


# --- Server Entry Point ---

if __name__ == "__main__":
    import uvicorn

    # Start the Uvicorn server (Default: http://127.0.0.1:8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
