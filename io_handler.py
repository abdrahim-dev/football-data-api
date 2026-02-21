"""
Input/Output handler module for the Football Data project.
Handles the conversion of raw data into DataFrames and manages file exports.
"""

import pandas as pd
from config import OUTPUT_DIR


def data_to_dataframe(data, filename):
    """
    Converts a list of dictionaries into a pandas DataFrame and exports it.

    The data is saved in two formats (CSV and JSON) within the configured
    output directory.

    Args:
        data (list[dict]): The list of data records to be saved.
        filename (str): The base name for the output files (without extension).

    Returns:
        pandas.DataFrame: The resulting DataFrame object for further processing.
    """
    # Create the DataFrame from the input data
    df = pd.DataFrame(data)

    # Print the DataFrame to the console for quick visual verification
    print(df)

    # Export to CSV format for Excel/Spreadsheet compatibility
    df.to_csv(f"{OUTPUT_DIR}/{filename}.csv", index=False)

    # Export to JSON format for web-friendly data structures
    df.to_json(f"{OUTPUT_DIR}/{filename}.json", orient="records", indent=2)

    return df
