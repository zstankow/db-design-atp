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


def get_tournament_id(cursor, tournament_name, year):
    """
    get the id of a tournament depending on a name and a year
    """
    query = "SELECT id FROM tournaments WHERE name = %s AND year = %s"
    cursor.execute(query, (tournament_name, year))
    row = cursor.fetchone()
    print(row[0])
    return row[0] if row else None


def insert_finals(finals_info):
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
                print(tournament_name, date[-4:])
                tournament_id = get_tournament_id(cursor, tournament_name, date[-4:])
                print(final_data)
                # Insert data into the tournaments table
                query_insert = ("INSERT INTO finals "
                                "(date, tournament_id, tournament_name, winner, loser, game_result) "
                                "VALUES (%s, %s, %s, %s, %s, %s)")
                cursor.execute(query_insert, (date, tournament_id, tournament_name, winner, loser, game_result))
                logger.info(f"Successfully inserted {tournament_name} {date} final into table.")
        except Exception as e:
            logger.info(f"{e}: Failed to insert final into table.")
    # Commit changes to the database
    connection.commit()


final_info = [["16-01-2023", "Australian Open", "Novak Djokovic", "Stefanos Tsitsipas", "6-3 7-6(4) 7-6(5)"],
              ["17-01-2023", "Roland Garros", "Novak Djokovic", "Alcaraz", "6-3 7-6(4) 7-6(5)"]]

insert_finals(final_info)
