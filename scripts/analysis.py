# scripts/analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

DB_PATH = os.path.join('db', 'cricket.db')
engine = create_engine(f"sqlite:///{DB_PATH}")

players = pd.read_sql("SELECT * FROM players", engine)
matches = pd.read_sql("SELECT * FROM matches", engine)
perf = pd.read_sql("SELECT * FROM performances", engine)

# Aggregations
runs_per_player = perf.groupby('player_id', as_index=False)['runs'].sum()
runs_per_player = runs_per_player.merge(players[['player_id','full_name']], on='player_id')

appearances = perf.groupby('player_id', as_index=False).size().reset_index(name='appearances')
batting = runs_per_player.merge(appearances, on='player_id')

balls = perf.groupby('player_id', as_index=False)['balls_faced'].sum()
batting = batting.merge(balls, on='player_id')
batting['avg_naive'] = batting['runs'] / batting['appearances']
batting['strike_rate'] = batting.apply(lambda r: (r['runs']/r['balls_faced']*100) if r['balls_faced']>0 else 0, axis=1)

print("=== Batting summary ===")
print(batting[['player_id','full_name','runs','appearances','avg_naive','balls_faced','strike_rate']].to_string(index=False))

# Player report function
def player_report(player_id):
    pinfo = players[players['player_id']==player_id].iloc[0].to_dict()
    pperf = perf[perf['player_id']==player_id].merge(matches, on='match_id')
    total_runs = pperf['runs'].sum()
    total_wickets = pperf['wickets'].sum()
    total_balls = pperf['balls_faced'].sum()
    appearances = len(pperf)
    avg = total_runs / appearances if appearances>0 else None
    sr = (total_runs/total_balls*100) if total_balls>0 else None
    report = {
        'player': pinfo['full_name'],
        'role': pinfo['role'],
        'total_runs': int(total_runs),
        'total_wickets': int(total_wickets),
        'appearances': appearances,
        'batting_avg_naive': avg,
        'strike_rate': sr,
        'match_details': pperf[['match_id','date','opponent','runs','balls_faced','wickets']].to_dict('records')
    }
    return report

# Visualizations directory
os.makedirs('plots', exist_ok=True)

def plot_runs_over_time(player_id):
    pperf = perf[perf['player_id']==player_id].merge(matches, on='match_id').sort_values('date')
    if pperf.empty:
        print('No data for', player_id)
        return
    plt.figure()
    plt.plot(pd.to_datetime(pperf['date']), pperf['runs'], marker='o')
    plt.title(f"Runs over time: {player_id}")
    plt.xlabel('Date')
    plt.ylabel('Runs')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'plots/runs_over_time_{player_id}.png')
    plt.close()

def plot_total_runs_bar():
    df = runs_per_player.sort_values('runs', ascending=True)
    plt.figure()
    plt.barh(df['full_name'], df['runs'])
    plt.title('Total runs per player')
    plt.xlabel('Runs')
    plt.tight_layout()
    plt.savefig('plots/total_runs_per_player.png')
    plt.close()

def plot_runs_histogram():
    plt.figure()
    plt.hist(perf['runs'], bins=range(0, 101, 10))
    plt.title('Distribution of runs per innings')
    plt.xlabel('Runs')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('plots/runs_histogram.png')
    plt.close()

# Generate plots and example report
plot_total_runs_bar()
plot_runs_histogram()
plot_runs_over_time('P001')

print('\nPlots saved in ./plots/')

# Example: filtering with pandas
high_performers = batting[(batting['appearances']>1) & (batting['avg_naive']>40)]
print('\nHigh performers (appearances>1 & avg>40):')
print(high_performers[['player_id','full_name','appearances','avg_naive']].to_string(index=False))

if __name__ == '__main__':
    print('\nExample player report for P001:')
    print(player_report('P001'))
