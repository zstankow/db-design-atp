import pymysql
import json

with open('config.json', 'r') as file:
    constants_data = json.load(file)

USER = constants_data['USER']
PASSWORD = constants_data['PASSWORD']


def connect_to_mysql():
    connect = pymysql.connect(
        host="localhost",
        user=USER,
        password=PASSWORD
    )
    cursor = connect.cursor()
    return connect, cursor
