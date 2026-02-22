# ⚽ Football Data Analysis Tool v2.0

A professional, modular Python application that fetches, processes, and visualizes football match data using the [football-data.org](https://www.football-data.org/) API.

---

## 🚀 Key Features

* **Automated Data Retrieval**: Fetches real-time match results, team metadata, and league standings for La Liga.
* **Performance Analytics**: Computes wins, draws, losses, and total matches played for specific teams within custom date ranges.
* **Dual-Format Export**: Automatically saves all processed data into both `CSV` (for Excel) and `JSON` (for web/apps) formats.
* **Visual Insights**: Generates high-quality `.png` pie charts of result distributions using Matplotlib.
* **Clean Architecture**: Built with a "Separation of Concerns" design, making it easy to add new features without breaking existing ones.
### 🌐 Web API Pro (`app.py`)
* **FastAPI Framework**: High-performance REST endpoints with automatic Swagger documentation.
* **Fuzzy Search**: Intelligent team discovery—finds "Real Madrid" even if you only type "Madrid".
* **Head-to-Head (H2H)**: A dedicated engine that compares two rival teams and calculates historical dominance.
* **Interactive Docs**: Built-in UI to test the API directly from your browser.

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

pip install requests pandas matplotlib python-dotenv uvicorn fastapi
or with uv: uv add requests pandas matplotlib python-dotenv uvicorn fastapi

### 3. Project structure:
football-data-api/
│
├── .env                # API Keys (Excluded from version control)
├── main.py             # The "Orchestrator" (Application entry point)
├── api_client.py       # Handles all HTTP requests and API communication
├── processor.py        # Core logic & data calculations
├── exporter.py         # File persistence (CSV, JSON storage)
├── visualizer.py       # Data visualization, charts, and plots
└── app.py              # Web API application (FastAPI/Flask)