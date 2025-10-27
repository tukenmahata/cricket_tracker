"""
Cricket Tracker - Load CSV Data into MySQL Database
---------------------------------------------------
This script reads data from 3 CSV files:
    - players.csv
    - matches.csv
    - performances.csv

Then it loads them into MySQL tables:
    - players
    - matches
    - performances

Author: Your Name / School Project
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os

# ---------------------------------------------------------------------
# 1. Database connection details
# ---------------------------------------------------------------------
DB_USER = "root"       # MySQL username
DB_PASS = ""    # MySQL password
DB_HOST = "localhost"          # Host (use 127.0.0.1 if localhost fails)
DB_NAME = "cricket"         # Database name

# ---------------------------------------------------------------------
# 2. CSV file locations (make sure files exist in 'data' folder)
# ---------------------------------------------------------------------
CSV_PLAYERS = os.path.join('data', 'players.csv')
CSV_MATCHES = os.path.join('data', 'matches.csv')
CSV_PERF = os.path.join('data', 'performances.csv')

# ---------------------------------------------------------------------
# 3. Create SQLAlchemy engine for MySQL
# ---------------------------------------------------------------------
# "mysql+mysqlconnector://" is the connection dialect for MySQL
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
    echo=False
)

# ---------------------------------------------------------------------
# 4. Helper function to load a CSV into a table
# ---------------------------------------------------------------------
def load_csv_to_table(csv_path, table_name):
    """Load CSV data into MySQL table using pandas."""
    print(f"Loading {csv_path} → {table_name} ...")
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"✅ Loaded {len(df)} records into {table_name}")

# ---------------------------------------------------------------------
# 5. Main logic
# ---------------------------------------------------------------------
def main():
    print("Starting data load process...")

    # Step 1: Disable foreign key checks so we can truncate safely
    with engine.begin() as conn:
        print("Truncating old data...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        conn.execute(text("TRUNCATE TABLE performances;"))
        conn.execute(text("TRUNCATE TABLE matches;"))
        conn.execute(text("TRUNCATE TABLE players;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
        print("Tables truncated successfully.")

    # Step 2: Load new CSV data into MySQL
    load_csv_to_table(CSV_PLAYERS, 'players')
    load_csv_to_table(CSV_MATCHES, 'matches')
    load_csv_to_table(CSV_PERF, 'performances')

    print("🎉 All CSV files successfully loaded into MySQL database!")

# ---------------------------------------------------------------------
# 6. Run the script
# ---------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("❌ Error while loading data:", e)
