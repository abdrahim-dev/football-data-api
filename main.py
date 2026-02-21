"""
Main entry point for the Football Data Analysis Tool.
Orchestrates the data fetching, processing, exporting, and visualization workflow.
"""

import sys
from datetime import datetime
import api_client
import processor
import io_handler
import visualizer


def get_date_range():
    """
    Prompts the user for a date range and validates the input format.

    Returns:
        tuple: (start_date_str, end_date_str) in YYYY-MM-DD format.
    """
    try:
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")

        # Validation: Try to parse the strings to ensure they are valid dates
        datetime.strptime(start_date_str, "%Y-%m-%d")
        datetime.strptime(end_date_str, "%Y-%m-%d")

        return start_date_str, end_date_str
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        sys.exit(1)


def main():
    """
    Execution logic for the football data pipeline.
    """
    # Team Selection (Future feature: implement a dynamic menu here)
    try:
        fav_team_id = int(input("Your favorite team ID: "))
    except ValueError:
        print("Error: Team ID must be a number.")
        sys.exit(1)

    # 1. Data Retrieval
    print("\nFetching data from API...")
    start_date, end_date = get_date_range()
    results = api_client.get_results_fav_team(start_date, end_date, fav_team_id)

    # 2. Raw Data Export
    # Save match results immediately after fetching
    io_handler.data_to_dataframe(results, "results_of_matches")

    # 3. Statistics Computation
    # Map IDs to names and calculate performance metrics
    team_map = api_client.get_team_mapping()
    team_name = team_map.get(fav_team_id, "Unknown Team")

    stats = processor.compute_team_stats(results, fav_team_id)
    stats["team_id"] = fav_team_id
    stats["team_name"] = team_name

    # 4. Statistics Export
    # Store the calculated metrics as CSV and JSON
    io_handler.data_to_dataframe([stats], f"{team_name}_statistics")

    # 5. Visualization
    # Generate and display the results pie chart
    visualizer.plot_team_stats_pie(stats, team_name)

    # 6. Supplementary Data
    # Fetch and save general league information and standings
    print("\nExporting general league data...")
    teams = api_client.get_football_teams()
    io_handler.data_to_dataframe(teams, "football_teams")

    standings = api_client.get_league_standings()
    io_handler.data_to_dataframe(standings, "league_standing")

    print("\nProcess completed successfully. Check the 'output' folder.")


if __name__ == "__main__":
    main()
