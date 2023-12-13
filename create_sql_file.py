# Define the SQL schema
sql_script = '''
-- Create players table
CREATE TABLE players (
    name VARCHAR(255) PRIMARY KEY,
    best_rank INTEGER,
    country_id INTEGER
);

-- Create tournaments table
CREATE TABLE tournaments (
    id INTEGER PRIMARY KEY,
    year INTEGER,
    name VARCHAR(255),
    level INTEGER,
    surface INTEGER,
    winner VARCHAR(255),
    finalist VARCHAR(255),
    no_events INTEGER,
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
'''

# Write the SQL script to a .sql file
with open('tennis_database.sql', 'w') as file:
    file.write(sql_script)

print("SQL file 'tennis_database.sql' created successfully.")