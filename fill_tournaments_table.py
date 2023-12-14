import tournaments
from connect_to_mysql import connect_to_mysql
import json
import pymysql

with open('config.json', 'r') as file:
    constants_data = json.load(file)

START = constants_data['START']
END = constants_data['END']
USER = constants_data['USER']
PASSWORD = constants_data['PASSWORD']


def get_tournament_info():
    for year in range(START, END, -1):
        tournaments_info = tournaments.run(str(year))
        insert_tournaments(tournaments_info)



def insert_tournaments(tournaments_info):
    connection = pymysql.connect(
        host="localhost",
        user=USER,
        password=PASSWORD,
        database="tennis")
    with connection.cursor() as cursor:
        for tournament_data in tournaments_info:
            # Extracting tournament data
            name, level, surface, year,participation_perc, strength, avg_elo, winner = tournament_data

            # Insert data into the tournaments table
            query_insert = "INSERT INTO tournaments (name, level, surface, year, participation_perc, strength, avg_elo, winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_insert,
                           (name, level, surface, int(year), float(participation_perc[:-1]) / 100, int(strength), avg_elo, winner))
            print("Row inserted successfully!")
    # Commit changes to the database
    connection.commit()
