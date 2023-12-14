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


def add_players_info():
    """
    Retrieves info on player rankings from the START year to the END year and inserts the data to the database.
    """
    for year in range(conf["START"], conf["END"], -1):
        players_info = webscraper.run_rankings(conf["NUM"], str(year))
        insert_players(players_info)
        logger.info(f"Player ranking information of year {year} added to database.")
        print(f"Tournament information of year {year} added to database.")


def insert_players(players_info):
    """
    Inserts player ranking data into the database.
    """
    connection = connect_to_mysql()
    with connection.cursor() as cursor:
        for player_data in players_info:
            # Check if the name already exists in the players table
            query_check = "SELECT COUNT(*) FROM players WHERE name = %s"
            cursor.execute(query_check, (player_data[2],))
            player_count = cursor.fetchone()[0]

            if not player_count:
                # Insert data into the players table
                query_insert = "INSERT INTO players (name, best_rank, country_id) VALUES (%s, %s, %s)"
                cursor.execute(query_insert, (player_data[conf["NAME"]], int(player_data[conf["BEST_RANK"]]),
                                              player_data[conf["COUNTRY"]]))
                logger.info(f"New player '{player_data[2]}' inserted into table")
            else:
                logger.info(f"Player '{player_data[2]}' already exists in the table.")

    # Commit changes to the database
    connection.commit()


def add_tournament_info():
    """
    Retrieves info on tournaments from the START year to the END year and inserts the data to the database.
    """
    for year in range(conf['START'], conf['END'], -1):
        tournaments_info = webscraper.run_tournaments(str(year))
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
            for tournament_data in tournaments_info:
                # Extracting tournament data
                name, level, surface, year, participation_perc, strength, avg_elo, winner = tournament_data

                # Insert data into the tournaments table
                query_insert = ("INSERT INTO tournaments "
                                "(name, level, surface, year, participation_perc, strength, avg_elo, winner) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(query_insert,
                               (name, level, surface, int(year), float(participation_perc[:-1]) / 100,
                                int(strength),
                                avg_elo, winner))
                logger.info(f"Successfully inserted '{name}' tournament into table.")
        except Exception as e:
            logger.info(f"{e}: Failed to insert tournament into table.")
    # Commit changes to the database
    connection.commit()
