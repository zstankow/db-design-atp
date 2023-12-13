import pymysql

# Establish a connection to the MySQL database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="nathszpil97",
    database="tennis"
)


def insert_player_in_table(player_data):
    with connection.cursor() as cursor:
        # Check if the name already exists in the players table
        query_check = "SELECT COUNT(*) FROM players WHERE name = %s"
        cursor.execute(query_check, (player_data['name'],))
        player_count = cursor.fetchone()[0]

        if player_count == 0:
            # Insert data into the players table
            query_insert = "INSERT INTO players (name, best_rank, country_id) VALUES (%s, %s, %s)"
            cursor.execute(query_insert, (player_data['name'], player_data['best rank'], player_data['country']))
            print("Row inserted successfully!")
        else:
            print("Player already exists in the table.")

    # Commit changes to the database
    connection.commit()


row_data = {'ranking': '2', 'best rank': '1', 'country': 'SUI', 'name': 'Roger Federer', '+/- position': '-',
            '+/- points': '-'}

insert_player_in_table(row_data)
