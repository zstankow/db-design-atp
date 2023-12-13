import pymysql

# Establish a connection to the MySQL database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="nathszpil97",
    database="tennis"
)


def fill_table(row_data):
    try:
        # Create a cursor object
        with connection.cursor() as cursor:
            # Insert data into the players table
            query_insert = "INSERT INTO players (name, best_rank, country_id) VALUES (%s, %s, %s)"
            cursor.execute(query_insert, (row_data['name'], row_data['best rank'], row_data['country']))

            print("Row inserted successfully!")

        # Commit changes to the database
        connection.commit()

    finally:
        # Close the database connection
        connection.close()
