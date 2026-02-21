# ⚽ Football Data Analysis Tool v2.0

A professional, modular Python application that fetches, processes, and visualizes football match data using the [football-data.org](https://www.football-data.org/) API.

---

## 🚀 Key Features

* **Automated Data Retrieval**: Fetches real-time match results, team metadata, and league standings for La Liga.
* **Performance Analytics**: Computes wins, draws, losses, and total matches played for specific teams within custom date ranges.
* **Dual-Format Export**: Automatically saves all processed data into both `CSV` (for Excel) and `JSON` (for web/apps) formats.
* **Visual Insights**: Generates high-quality `.png` pie charts of result distributions using Matplotlib.
* **Clean Architecture**: Built with a "Separation of Concerns" design, making it easy to add new features without breaking existing ones.

---

## 🏗️ Architecture Overview

The project is structured to separate data fetching, logic, and output:



* **API Client**: Handles all HTTP communication and authentication.
* **Processor**: Calculates statistics (Wins/Losses) and formats raw data.
* **I/O Handler**: Manages file creation and DataFrame conversions.
* **Visualizer**: Handles graphical plotting logic.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have at least **Python 3.14** installed on your system.

### 2. Install Dependencies
Run the following command to install all necessary libraries:

pip install requests pandas matplotlib python-dotenv

### 3. Project structure:
football-data-api/
│
├── .env                # API Keys
├── main.py             # Der "Dirigent" (startet das Programm)
├── api_client.py       # Alles rund um HTTP-Anfragen
├── processor.py        # Logik & Berechnungen
├── exporter.py         # Speichern von Dateien (CSV, JSON)
├── visualizer.py       # Diagramme und Plots
└── utils.py            # Hilfsfunktionen (z.B. User-Input)