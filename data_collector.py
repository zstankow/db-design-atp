import webscraper
import pymysql
import json
from tennis_logger import logger

with open('config.json', 'r') as file:
    conf = json.load(file)


def connect_to_mysql():
    """
    Connects to pymysql with username and password.
    Returns connection.
    """
    connection = pymysql.connect(
        host="localhost",
        user=conf["USER"],
        password=conf["PASSWORD"],
        database=conf["DATABASE"]
    )
    return connection


def add_events_info():
    """
    Retrieves info on tournament events from between years 2014 and 2023.
    """
    events_info = webscraper.scrape_events()
    insert_events(events_info)
    logger.info(f"Event information of added to database.")
    print(f"Event information of added to database.")


def get_player_id(player_name, connection):
    """
    Returns player_id of player.
    """
    with connection.cursor() as cursor:
        query_player = "SELECT player_id FROM players WHERE name = %s"
        cursor.execute(query_player, player_name)
        player_id = cursor.fetchone()
        return player_id


def get_tournament_id(tournament_name, connection):
    """
    Returns tournament_id of tournament.
    """
    with connection.cursor() as cursor:
        query_player = "SELECT tournament_id FROM tournaments WHERE name = %s"
        cursor.execute(query_player, tournament_name)
        tournament_id = cursor.fetchone()
        return tournament_id


def insert_events(events_info):
    """
    Inserts events data into events table.
    """
    connection = connect_to_mysql()
    with connection.cursor() as cursor:
        for index, event_data in events_info.iterrows():
            # Check if the name already exists in the players table
            winner_id = get_player_id(event_data["Winner"], connection)
            finalist_id = get_player_id(event_data["Finalist"], connection)
            tournament_id = get_tournament_id(event_data["Name"], connection)

            # Insert data into the events table
            query_insert = ("INSERT INTO events (date, name, tournament_id, winner_id, finalist_id, game_result) "
                            "VALUES (%s, %s, %s, %s, %s, %s)")
            cursor.execute(query_insert, (event_data["Date"], event_data["Name"], tournament_id,
                                          winner_id, finalist_id, event_data["Score"]))
            logger.info(f"New event '{event_data['Name']}' inserted into table")
        else:
            logger.info(f"Player '{event_data['Name']}', year '{event_data['Date']}' failed to be inserted into table.")

    # Commit changes to the database
    connection.commit()


def add_players_info():
    """
    Retrieves info on player rankings from the START year to the END year and inserts the data to the database.
    """
    for year in range(conf["START"], conf["END"], -1):
        players_info = webscraper.scrape_rankings(conf["NUM"], str(year))
        insert_players(players_info)
        logger.info(f"Players ranking information of year {year} added to database.")
        print(f"Players ranking information of year {year} added to database.")


def insert_countries(player_data, connection):
    """
    Inserts country name into countries table.
    """
    with connection.cursor() as cursor:
        query_country = "SELECT country_id FROM countries WHERE name = %s"
        cursor.execute(query_country, (player_data["Country"]))
        country_result = cursor.fetchone()

        if country_result:
            country_id = country_result[0]
        else:
            # Insert country into countries table and get the generated country_id
            query_insert_country = "INSERT INTO countries (name) VALUES (%s)"
            cursor.execute(query_insert_country, (player_data["Country"]))
            country_id = cursor.lastrowid
    connection.commit()
    return country_id


def insert_players(players_info):
    """
    Inserts player ranking data into the database.
    """
    connection = connect_to_mysql()
    with connection.cursor() as cursor:
        for index, player_data in players_info.iterrows():
            # Check if the name already exists in the players table
            query_check = "SELECT COUNT(*) FROM players WHERE name = %s"
            cursor.execute(query_check, (player_data["Name"]))
            player_count = cursor.fetchone()[0]

            if not player_count:
                # Insert country id
                country_id = insert_countries(player_data, connection)
                # Insert data into the players table
                query_insert = "INSERT INTO players (name, best_rank, country_id) VALUES (%s, %s, %s)"
                cursor.execute(query_insert, (player_data["Name"], int(player_data["Best Ranking"]),
                                              country_id))
                logger.info(f"New player '{player_data['Name']}' inserted into table")
            else:
                logger.info(f"Player '{player_data['Name']}' already exists in the table.")

    # Commit changes to the database
    connection.commit()


def add_tournament_info():
    """
    Retrieves info on tournaments from the START year to the END year and inserts the data to the database.
    """
    for year in range(conf['START'], conf['END'], -1):
        tournaments_info = webscraper.scrape_tournaments(str(year))
        insert_tournaments(tournaments_info)
        logger.info(f"Tournament information of year {year} added to database.")
        print(f"Tournament information of year {year} added to database.")


def insert_tournaments(tournaments_info):
    """
    Inserts tournament data into the database.
    """
    connection = connect_to_mysql()
    logger.info("Connected to pymysql")
    with connection.cursor() as cursor:
        try:
            for index, tournament_data in tournaments_info.iterrows():
                # Extracting tournament data
                year = int(tournament_data["Seasons"])
                participation_perc = float(tournament_data["Part"][:-1])
                strength = int(tournament_data["Str."])

                # Insert data into the tournaments table
                query_insert = ("INSERT INTO tournaments "
                                "(name, level, surface, year, participation_perc, strength, avg_elo) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(query_insert, (tournament_data["Name"], tournament_data["Level"],
                                              tournament_data["Surface"], year, participation_perc,
                                              strength, tournament_data["Elo."]))
                logger.info(f"Successfully inserted '{tournament_data['Name']}' tournament into table.")
        except Exception as e:
            logger.info(f"{e}: Failed to insert tournament into table.")
    # Commit changes to the database
    connection.commit()
