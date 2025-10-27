# scripts/load_to_mysql.py
import pandas as pd
from sqlalchemy import create_engine
import os

# Config - change user/pass if different
DB_USER = "root"
DB_PASS = ""
DB_HOST = "localhost"
DB_NAME = "cricket"

# Files
CSV_PLAYERS = os.path.join('data', 'players.csv')
CSV_MATCHES = os.path.join('data', 'matches.csv')
CSV_PERF = os.path.join('data', 'performances.csv')

# SQLAlchemy engine for MySQL using mysql+mysqlconnector
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}", echo=False)

def load_csv_to_table(csv_path, table_name, dtype_map=None):
    df = pd.read_csv(csv_path)
    # Optionally enforce datatypes
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

def main():
    # If running repeatedly, you may want to truncate tables first
    with engine.begin() as conn:
        conn.execute("SET FOREIGN_KEY_CHECKS=0;")
        conn.execute("TRUNCATE TABLE performances;")
        conn.execute("TRUNCATE TABLE matches;")
        conn.execute("TRUNCATE TABLE players;")
        conn.execute("SET FOREIGN_KEY_CHECKS=1;")

    load_csv_to_table(CSV_PLAYERS, 'players')
    load_csv_to_table(CSV_MATCHES, 'matches')
    load_csv_to_table(CSV_PERF, 'performances')
    print("Loaded CSVs into MySQL database.")

if __name__ == "__main__":
    main()
