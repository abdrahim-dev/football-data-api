"""
Data processing module for football statistics.
Contains logic to calculate performance metrics from raw match data.
"""


def compute_team_stats(results, team_id):
    """
    Calculates total wins, draws, losses, and matches played for a specific team.

    This function iterates through match results and determines the outcome
    by comparing 'goals for' vs 'goals against' based on whether the team
    played at home or away.

    Args:
        results (list[dict]): A list of match dictionaries containing scores and IDs.
        team_id (int): The unique ID of the team to calculate stats for.

    Returns:
        dict: A dictionary containing 'wins', 'draws', 'losses', and 'matches_played'.
    """
    # Initialize the statistics counter
    stats = {"wins": 0, "draws": 0, "losses": 0}

    for match in results:
        # Determine goal counts based on team's role in the match (Home or Away)
        if team_id == match["home_team_id"]:
            goals_for, goals_against = match["home_score"], match["away_score"]
        elif team_id == match["away_team_id"]:
            goals_for, goals_against = match["away_score"], match["home_score"]
        else:
            # Skip matches that do not involve the selected team
            continue

        # Comparison logic to determine match outcome
        if goals_for > goals_against:
            stats["wins"] += 1
        elif goals_for < goals_against:
            stats["losses"] += 1
        else:
            stats["draws"] += 1

    # Calculate total matches played from the accumulated stats
    stats["matches_played"] = stats["wins"] + stats["draws"] + stats["losses"]

    return stats
