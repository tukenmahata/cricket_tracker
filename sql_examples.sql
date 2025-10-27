-- SQL schema (SQLite)
CREATE TABLE IF NOT EXISTS players (
  player_id TEXT PRIMARY KEY,
  full_name TEXT NOT NULL,
  role TEXT,
  birth_date DATE,
  state TEXT
);

CREATE TABLE IF NOT EXISTS matches (
  match_id TEXT PRIMARY KEY,
  date DATE,
  opponent TEXT,
  venue TEXT,
  tournament TEXT
);

CREATE TABLE IF NOT EXISTS performances (
  perf_id TEXT PRIMARY KEY,
  match_id TEXT,
  player_id TEXT,
  runs INTEGER DEFAULT 0,
  balls_faced INTEGER DEFAULT 0,
  fours INTEGER DEFAULT 0,
  sixes INTEGER DEFAULT 0,
  wickets INTEGER DEFAULT 0,
  overs REAL DEFAULT 0,
  maiden INTEGER DEFAULT 0,
  balls_bowled INTEGER DEFAULT 0,
  runs_conceded INTEGER DEFAULT 0,
  catches INTEGER DEFAULT 0,
  stumpings INTEGER DEFAULT 0,
  not_out INTEGER DEFAULT 0,
  FOREIGN KEY(match_id) REFERENCES matches(match_id),
  FOREIGN KEY(player_id) REFERENCES players(player_id)
);

CREATE INDEX IF NOT EXISTS idx_perf_player ON performances(player_id);
CREATE INDEX IF NOT EXISTS idx_perf_match ON performances(match_id);

-- Example query: total runs per player
SELECT p.player_id, p.full_name, SUM(perf.runs) AS total_runs
FROM performances perf
JOIN players p ON p.player_id = perf.player_id
GROUP BY p.player_id
ORDER BY total_runs DESC;
