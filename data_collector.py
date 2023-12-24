import webscraper
import pymysql
import json
import pandas as pd
from instagrapi import Client
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
        user=conf["MYSQL_USER"],
        password=conf["MYSQL_PASSWORD"],
        database=conf["DATABASE"]
    )
    return connection


def connect_to_instagram():
    """
       Connects to instagram with username and password.
       Returns client.
    """
    print("Connecting to Instagram...")
    client = Client()
    client.login(conf["INSTA_USERNAME"], conf["INSTA_PASSWORD"])
    print("Connected")
    return client


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
                participation_perc = float(tournament_data["Part"][:-1]) / 100
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


def get_account_id(cursor, username):
    """
    get the account id by the username
    """
    account_id = None
    select_query = "SELECT id FROM accounts WHERE username = %s"
    cursor.execute(select_query, (username,))
    result = cursor.fetchone()
    if result:
        account_id = result[conf["ACCOUNT_ID_INDEX"]]
    return account_id


def insert_usernames(connection):
    """
    insert all the usernames that are written in players_usernames.csv file in the table accounts
    """
    try:
        data = pd.read_csv('players_usernames.csv')
        with connection.cursor() as cursor:
            delete_accounts_query = "DELETE FROM accounts"
            delete_posts_query = "DELETE FROM posts"
            cursor.execute(delete_posts_query)
            cursor.execute(delete_accounts_query)
            for index, row in data.iterrows():
                player_name = row['Player Name']
                username = row['Username']

                # Get player_id from the players table based on player_name
                query_player_id = "SELECT id FROM players WHERE name = %s"
                cursor.execute(query_player_id, (player_name,))
                player_id = cursor.fetchone()  # Fetch the row
                if player_id:  # Ensure a result was obtained
                    player_id = player_id[conf["PLAYER_ID_INDEX"]]  # Access the first column value in the tuple
                    # Insert username and player_id into the accounts table
                    insert_query = "INSERT INTO accounts (username, player_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (username, player_id))
                    connection.commit()
        print("Usernames inserted successfully!")
    except pymysql.Error as error:
        print("Error inserting usernames:", error)


def insert_posts_infos(client, cursor, username):
    """
    To fill the sql table posts by taking the N_POSTS last posts
    """
    user_id = client.user_id_from_username(username)
    last_10_posts = client.user_medias(user_id, conf["N_POSTS"])
    account_id = get_account_id(cursor, username)
    for post in last_10_posts:
        like_count = post.like_count
        comment_count = post.comment_count
        caption_text = post.caption_text[:conf["CAPTION_LIMIT"]]
        url = conf["INSTA_URL"] + post.code
        insert_query = """
            INSERT INTO posts (account_id, username, text, likes, comments, url)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        insert_values = (account_id, username, caption_text, like_count, comment_count, url)
        cursor.execute(insert_query, insert_values)


def insert_account_infos(client, cursor, username):
    """
    To fill the sql account table
    """
    user = client.user_info_by_username(username)
    follower_count = user.follower_count
    following_count = user.following_count
    posts_count = user.media_count
    update_query = """
                UPDATE accounts
                SET followers = %s, following = %s, total_posts = %s
                WHERE username = %s
                """
    update_values = (follower_count, following_count, posts_count, username)
    cursor.execute(update_query, update_values)


def add_insta_info():
    """
    function to fill the sql tables related to Instagram : accounts and posts
    """
    connection = connect_to_mysql()
    client = connect_to_instagram()
    insert_usernames(connection)
    try:
        with connection.cursor() as cursor:
            # Fetch all usernames from the accounts table
            select_query = "SELECT username FROM accounts"
            cursor.execute(select_query)
            usernames = cursor.fetchall()
            for username in usernames:
                username = username[conf["USERNAME_INDEX"]]
                insert_account_infos(client, cursor, username)
                insert_posts_infos(client, cursor, username)
                connection.commit()
                print(f"{username} instagram infos added")

    except pymysql.Error as error:
        print("Error fetching usernames:", error)
