USE cricket;

CREATE TABLE IF NOT EXISTS players (
  player_id VARCHAR(50) PRIMARY KEY,
  full_name VARCHAR(100) NOT NULL,
  role VARCHAR(50),
  birth_date DATE,
  state VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS matches (
  match_id VARCHAR(50) PRIMARY KEY,
  date DATE,
  opponent VARCHAR(100),
  venue VARCHAR(100),
  tournament VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS performances (
  perf_id VARCHAR(50) PRIMARY KEY,
  match_id VARCHAR(50),
  player_id VARCHAR(50),
  runs INT DEFAULT 0,
  balls_faced INT DEFAULT 0,
  fours INT DEFAULT 0,
  sixes INT DEFAULT 0,
  wickets INT DEFAULT 0,
  overs DECIMAL(4,1) DEFAULT 0.0,
  maiden INT DEFAULT 0,
  balls_bowled INT DEFAULT 0,
  runs_conceded INT DEFAULT 0,
  catches INT DEFAULT 0,
  stumpings INT DEFAULT 0,
  not_out INT DEFAULT 0,
  FOREIGN KEY (match_id) REFERENCES matches(match_id),
  FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE INDEX idx_perf_player ON performances (player_id);
CREATE INDEX idx_perf_match ON performances (match_id);
