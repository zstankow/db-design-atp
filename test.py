import pymysql
import pandas as pd

def connect_to_mysql():
    # Replace the placeholders with your actual database credentials
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='tennis',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
def get_players_not_in_csv(csv_filename):
    connection = connect_to_mysql()

    try:
        with connection.cursor() as cursor:
            # Fetch player names and their best ranks from the database
            select_query = "SELECT name, best_rank FROM players"
            cursor.execute(select_query)
            players_data = cursor.fetchall()

            # Read player names from the specified CSV file
            csv_data = pd.read_csv(csv_filename)
            players_in_csv = csv_data['Player Name'].tolist()

            # Create a dictionary to store the best ranks for each player
            best_ranks = {player['name']: player['best_rank'] for player in players_data}

            # Find players that are in the database but not in the CSV file
            players_not_in_csv = [player for player in best_ranks.keys() if player not in players_in_csv]

            # Print the names of players not in the CSV file and their best ranks
            if players_not_in_csv:
                print("Players not in the CSV file:")
                for player in players_not_in_csv:
                    print(f"Player: {player}, Best Rank: {best_ranks[player]}")
            else:
                print("All players are in the CSV file.")

    except pymysql.Error as error:
        print("Error fetching player names:", error)

    finally:
        connection.close()

# Example usage:
csv_file = 'players_usernames.csv'  # Replace with your CSV file name
get_players_not_in_csv(csv_file)