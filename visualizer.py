"""
Visualization module for the Football Data project.
Provides functions to generate graphical representations of team statistics.
"""

import matplotlib.pyplot as plt
from config import OUTPUT_DIR


def plot_team_stats_pie(stats, team_name):
    """
    Generates and saves a pie chart showing the distribution of match results.

    Args:
        stats (dict): Dictionary containing 'wins', 'draws', and 'losses'.
        team_name (str): Name of the team to be used in the title and filename.
    """
    # Define chart categories and their corresponding data values
    labels = ["Wins", "Draws", "Losses"]
    values = [stats["wins"], stats["draws"], stats["losses"]]

    # Professional color scheme: Green for wins, Amber for draws, Red for losses
    colors = ["#22D428", "#FFBF00", "#FB3333"]

    # Initialize the plot figure
    plt.figure()

    # Create the pie chart with percentage formatting and a 90-degree start angle
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)

    # Add descriptive metadata to the plot
    plt.title(f"Results Distribution for {team_name}")

    # Ensure the pie is drawn as a circle (equal aspect ratio)
    plt.axis("equal")

    # Place the legend for better readability
    plt.legend(labels, loc="upper right")

    # Save the resulting visualization to the output directory
    plt.savefig(f"{OUTPUT_DIR}/{team_name}_stats_pie_chart.png")

    # Adjust layout to prevent clipping and display the plot
    plt.tight_layout()
    plt.show()
