<<<<<<< HEAD
from instagrapi import Client
=======
import argparse
import json
from tennis_logger import logger
from data_collector import add_players_info, add_tournament_info, add_events_info
from insta_api import add_posts_info
import webscraper
>>>>>>> c8804a6661b70329fc53200183ee35b5a2aabfa1
import pymysql

# Connect to MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='tennis'
)

# Create a cursor
cursor = connection.cursor()

username = "nathanszpilman"
password = "azeqsd"

client = Client()
client.login(username, password)

target_usernames = ["djokernole", "k1ngkyrg1os"]


def connect_to_instagram(username, password):
    client = Client()
    client.login(username, password)
    return client


def insert_account_infos(user, cursor, username):
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


def insert_posts_infos(client, user, cursor, username):
    last_10_posts = client.user_medias(user.pk, 10)
    for post in last_10_posts:
        like_counts = post.like_count
        comment_count = post.comment_count
        caption_text = post.caption_text[0:20]
        url = "https://www.instagram.com/p/" + post.code

        # SQL INSERT query to add a new row for each post into the 'posts' table
        insert_query = """
            INSERT INTO posts (account_name, text, likes, comments, url)
            VALUES (%s, %s, %s, %s, %s)
            """
        insert_values = (username, caption_text, like_counts, comment_count, url)
        cursor.execute(insert_query, insert_values)

<<<<<<< HEAD
    connection.commit()
=======
    elif args.command == 'ranking':
        print(f"Executing 'ranking' command for the year {args.year} with {args.number_of_players} players")
        print("Loading...")
        table = webscraper.scrape_rankings(args.number_of_players, args.year)
        webscraper.print_ranking_data(table)

    elif args.command == 'empty_db':
        print(f"Creating empty database 'tennis'")
        execute_sql_file()
        print(f"Database 'tennis' created.")

    elif args.command == 'create_db':
        print(f"Creating database 'tennis'")
        execute_sql_file()
        print(f"Database 'tennis' created.")
        print(f"Collecting data... This will take a several minutes...")
        add_players_info()
        add_tournament_info()
        add_events_info()
        add_posts_info()


    else:
        print("Invalid command. Supported commands: tournaments, ranking, empty_db, create_db.")
>>>>>>> c8804a6661b70329fc53200183ee35b5a2aabfa1


def insert_insta_info_to_table(client, username, cursor):
    user = client.user_info_by_username(username)
    insert_account_infos(user, cursor, username)
    insert_posts_infos(client, user, cursor, username)
    connection.commit()


for user in target_usernames:
    insert_insta_info_to_table(client, user, cursor)
