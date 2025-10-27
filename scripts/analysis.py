"""
Cricket Tracker - Performance Analysis using MySQL, Pandas, and Matplotlib
---------------------------------------------------------------------------"""

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

# ---------------------------------------------------------------------
# 1. Database connection setup
# ---------------------------------------------------------------------
DB_USER = "root"       # must match your MySQL setup
DB_PASS = ""
DB_HOST = "localhost"
DB_NAME = "cricket"

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)

# ---------------------------------------------------------------------
# 2. Load tables from MySQL into pandas DataFrames
# ---------------------------------------------------------------------
print("📦 Loading data from MySQL...")

players = pd.read_sql("SELECT * FROM players", engine)
matches = pd.read_sql("SELECT * FROM matches", engine)
perf = pd.read_sql("SELECT * FROM performances", engine)

print(f"✅ Loaded {len(players)} players, {len(matches)} matches, {len(perf)} performance records.")

# ---------------------------------------------------------------------
# 3. Data analysis using pandas
# ---------------------------------------------------------------------
print("\n⚙️ Analyzing player performance...")

# Total runs and wickets per player
summary = perf.groupby('player_id', as_index=False).agg({
    'runs': 'sum',
    'balls_faced': 'sum',
    'wickets': 'sum',
    'not_out': 'sum'
})

# Add player name
summary = summary.merge(players[['player_id', 'full_name', 'role']], on='player_id', how='left')

# Calculate batting average and strike rate
summary['innings'] = perf.groupby('player_id')['perf_id'].count().values
summary['dismissals'] = summary['innings'] - summary['not_out']
summary['dismissals'] = summary['dismissals'].replace(0, pd.NA)
summary['batting_average'] = summary['runs'] / summary['dismissals']
summary['strike_rate'] = summary.apply(
    lambda r: (r['runs'] / r['balls_faced'] * 100) if r['balls_faced'] > 0 else 0,
    axis=1
)

# Sort players by total runs
summary = summary.sort_values(by='runs', ascending=False)

print("📊 Batting Summary:")
print(summary[['player_id', 'full_name', 'role', 'runs', 'wickets', 'batting_average', 'strike_rate']].to_string(index=False))

# ---------------------------------------------------------------------
# 4. Visualization (Matplotlib)
# ---------------------------------------------------------------------
os.makedirs('plots', exist_ok=True)

# Bar Chart - Total Runs per Player
plt.figure(figsize=(8,5))
plt.bar(summary['full_name'], summary['runs'], color='skyblue', edgecolor='black')
plt.title("Total Runs by Player")
plt.xlabel("Player")
plt.ylabel("Total Runs")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig('plots/total_runs_per_player.png')
plt.close()

# Histogram - Distribution of Runs per Innings
plt.figure(figsize=(8,5))
plt.hist(perf['runs'], bins=range(0, 101, 10), color='lightgreen', edgecolor='black')
plt.title("Distribution of Runs per Innings")
plt.xlabel("Runs Scored")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig('plots/runs_distribution.png')
plt.close()

print("Charts created in the 'plots' folder:")
print(" - total_runs_per_player.png")
print(" - runs_distribution.png")

# ---------------------------------------------------------------------
# 5. Individual player performance report
# ---------------------------------------------------------------------
def player_report(player_id):
    """Return detailed stats for a given player."""
    pinfo = players[players['player_id'] == player_id].iloc[0]
    pperf = perf[perf['player_id'] == player_id].merge(matches, on='match_id')

    total_runs = pperf['runs'].sum()
    total_wickets = pperf['wickets'].sum()
    total_balls = pperf['balls_faced'].sum()
    innings = len(pperf)
    not_outs = pperf['not_out'].sum()
    dismissals = innings - not_outs if innings > 0 else 0

    avg = round(total_runs / dismissals, 2) if dismissals > 0 else total_runs
    sr = round(total_runs / total_balls * 100, 2) if total_balls > 0 else 0

    print(" Player Performance Report:")
    print(f" Player Name : {pinfo['full_name']}")
    print(f" Role        : {pinfo['role']}")
    print(f" Total Runs  : {total_runs}")
    print(f" Total Wkts  : {total_wickets}")
    print(f" Innings     : {innings}")
    print(f" Not Outs    : {not_outs}")
    print(f" Average     : {avg}")
    print(f" Strike Rate : {sr}\n")

    print(" Match-wise Breakdown:")
    print(pperf[['match_id', 'date', 'opponent', 'runs', 'balls_faced', 'wickets']].to_string(index=False))

# Example report (you can test with any player_id like P001)
player_report('P001')

print("Analysis completed successfully!")
