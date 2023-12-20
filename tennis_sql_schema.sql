DROP DATABASE IF EXISTS tennis;
CREATE DATABASE tennis;
USE tennis;

-- Create players table
CREATE TABLE players (
    player_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    best_rank INTEGER,
    country_id INTEGER
);
    -- FOREIGN KEY (country_id) REFERENCES countries(country_id),

-- Create countries table
CREATE TABLE countries (
    country_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

-- Create tournaments table
CREATE TABLE tournaments (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    year INTEGER,
    name VARCHAR(255),
    level VARCHAR(255),
    surface VARCHAR(255),
    participation_perc FLOAT,
    strength INTEGER,
    avg_elo INTEGER
);

-- Create finals table
CREATE TABLE finals (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    date VARCHAR(255),
    tournament_id INTEGER,
    winner VARCHAR(255),
    loser VARCHAR(255),
    game_result VARCHAR(255)
);

CREATE TABLE accounts (
    player_id INTEGER
    username VARCHAR(255)
    followers INTEGER
    following INTEGER
    total_posts INTEGER
);

CREATE TABLE posts (
    id INTEGER AUTO_INCREMENT PRIMARY KEY
    account_name VARCHAR(255)
    text VARCHAR(255)
    likes INTEGER
    comments INTEGER
    url VARCHAR(255)
);
