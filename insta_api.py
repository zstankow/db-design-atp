from instagrapi import Client
import pymysql

# Connect to MySQL
connection = pymysql.connect(
    host='your_host',
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

target_username = "djokernole"


def insert_insta_info_to_table(client, username, cursor):
    user = client.user_info_by_username(username)
    follower_count = user.follower_count
    following_count = user.following_count
    posts_count = user.media_count

    update_query = """
            UPDATE accounts
            SET followers = %s, following = %s, total_posts = %s
            WHERE username = %s
            """
    update_values = (username, follower_count, following_count, posts_count)
    cursor.execute(update_query, update_values)
    connection.commit()
