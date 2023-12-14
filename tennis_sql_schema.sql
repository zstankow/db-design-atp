
    DROP DATABASE IF EXISTS tennis;
    CREATE DATABASE tennis;
    USE tennis;
    
    
    -- Create players table
    CREATE TABLE players (
        name VARCHAR(255) PRIMARY KEY,
        best_rank INTEGER,
        country_id VARCHAR(255)
    );

    -- Create tournaments table
    CREATE TABLE tournaments (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        year INTEGER,
        name VARCHAR(255),
        level VARCHAR(255),
        surface VARCHAR(255),
        winner VARCHAR(255),
        finalist VARCHAR(255),
        participation_perc FLOAT,
        strength INTEGER,
        avg_elo INTEGER
    );

    -- Create finals table
    CREATE TABLE finals (
        id INTEGER,
        winner VARCHAR(255),
        loser VARCHAR(255),
        FOREIGN KEY (id) REFERENCES tournaments(id),
        FOREIGN KEY (winner) REFERENCES players(name),
        FOREIGN KEY (loser) REFERENCES players(name),
        PRIMARY KEY (id, winner, loser)
    );
    