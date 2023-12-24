DROP DATABASE IF EXISTS tennis;
CREATE DATABASE tennis;
USE tennis;

-- Create players table
CREATE TABLE players (
    player_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    best_rank INTEGER,
    country_id INTEGER
    -- FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

-- Create countries table
CREATE TABLE countries (
    country_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

-- Create tournaments table
CREATE TABLE tournaments (
    tournament_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    year INTEGER,
    name VARCHAR(255),
    level VARCHAR(255),
    surface VARCHAR(255),
    participation_perc FLOAT,
    strength INTEGER,
    avg_elo INTEGER
);

-- Create events table
CREATE TABLE events (
    event_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    date DATE,
    tournament_id INTEGER,
    winner_id INTEGER,
    finalist_id INTEGER,
    game_result VARCHAR(255)
    -- FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id),
    -- FOREIGN KEY (winner_id) REFERENCES players(player_id),
    -- FOREIGN KEY (finalist_id) REFERENCES players(player_id),
);

-- Create posts table
CREATE TABLE posts (
    post_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    account_id INTEGER,
    text VARCHAR(255),
    likes INTEGER,
    comments INTEGER,
    url VARCHAR(255)
    -- FOREIGN KEY (account_id) REFERENCE accounts(account_id)
);

-- Create accounts table
CREATE TABLE accounts (
    account_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    player_id INTEGER
    -- FOREIGN KEY (player_id) REFERENCE players(player_id)
