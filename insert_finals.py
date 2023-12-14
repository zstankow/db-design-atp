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


final_info = [["16-01-2023", "Australian Open", "Novak Djokovic", "Stefanos Tsitsipas", "6-3 7-6(4) 7-6(5)"],
              ["17-01-2022", "Australian Open", "Novak Djokovic", "Stefanos Tsitsipas", "6-3 7-6(4) 7-6(5)"]]


def insert_tournaments(finals_info):
    """
    Inserts finals data into the database.
    """
    connection = connect_to_mysql()
    logger.info("Connected to pymysql")
    with connection.cursor() as cursor:
        try:
            for final_data in finals_info:
                # Extracting finals data
                date, tournament_name, winner, loser, game_result = final_data
                print(final_data)
                # Insert data into the tournaments table
                query_insert = ("INSERT INTO finals "
                                "(date, tournament_name, winner, loser, game_result) "
                                "VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(query_insert, (date, tournament_name, winner, loser, game_result))
                logger.info(f"Successfully inserted '{name}' final into table.")
        except Exception as e:
            logger.info(f"{e}: Failed to insert final into table.")
    # Commit changes to the database
    connection.commit()


insert_tournaments(final_info)
