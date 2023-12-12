import sqlite3

# Create or connect to a SQLite database
conn = sqlite3.connect('tennis.db')
cursor = conn.cursor()

# Create the players table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        name TEXT PRIMARY KEY,
        best_rank INTEGER,
        country_id INTEGER
    )
''')

# Create the tournaments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tournaments (
        id INTEGER PRIMARY KEY,
        year INTEGER,
        name TEXT,
        level INTEGER,
        surface INTEGER,
        winner TEXT,
        finalist TEXT,
        no_events INTEGER,
        participation_perc REAL,
        strength INTEGER,
        avg_elo INTEGER
    )
''')

# Create the finals table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS finals (
        id INTEGER,
        winner TEXT,
        loser TEXT,
        FOREIGN KEY (id) REFERENCES tournaments(id),
        FOREIGN KEY (winner) REFERENCES players(name),
        FOREIGN KEY (loser) REFERENCES players(name),
        PRIMARY KEY (id, winner, loser)
    )
''')

# Create the reference between tournaments' winner and players' name
cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS reference_trigger
    BEFORE INSERT ON finals
    FOR EACH ROW
    BEGIN
        SELECT RAISE(ROLLBACK, 'Player does not exist in players table')
        WHERE NEW.winner NOT IN (SELECT name FROM players);
    END;
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created successfully.")
