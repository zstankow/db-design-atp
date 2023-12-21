from instagrapi import Client
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


def insert_account_info(user, cursor, username):
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


def insert_posts_info(client, user, cursor, username):
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

    connection.commit()


def insert_insta_info_to_table(client, username, cursor):
    user = client.user_info_by_username(username)
    insert_account_info(user, cursor, username)
    insert_posts_info(client, user, cursor, username)
    connection.commit()


for user in target_usernames:
    insert_insta_info_to_table(client, user, cursor)