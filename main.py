import rankings
import tournaments
from create_sql_file import create_sql_file
import argparse
from connect_to_mysql import connect_to_mysql

from fill_players_table import insert_players
from fill_tournaments_table import insert_tournaments


def execute_sql_file():
    connection, cursor = connect_to_mysql()
    try:
        with open('tennis_database.sql', 'r') as file:
            sql_commands = file.read()
            # Split SQL commands by semicolon
            commands = sql_commands.split(';')
            for command in commands:
                # Skip empty commands
                if command.strip() != '':
                    cursor.execute(command)
        connection.commit()
        print("SQL file executed successfully!")
    except Exception as e:
        print("Error executing SQL file:", e)
    finally:
        connection.close()


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='User can type one of two arguments: [tournament year] \n'
                                                 'to webscrape data on tournaments from a specific year or \n'
                                                 '[ranking year number_of_players] \n'
                                                 ' to show the x ranked top players from a specific year')

    # Add command-line arguments
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Subparser for 'tournaments' command
    parser_tournaments = subparsers.add_parser('tournaments', help='Prints all tournaments from a specified year')
    parser_tournaments.add_argument('year', type=str, default='2023', help='Year of the tournaments')

    # Subparser for 'ranking' command
    parser_ranking = subparsers.add_parser('ranking', help='Prints ranking of top x players from a specified year')
    parser_ranking.add_argument('year', type=str, help='Year of the ranking')
    parser_ranking.add_argument('number_of_players', type=str, help='Number of players for the ranking')

    # Subparser for 'empty_db' command
    subparsers.add_parser('empty_db', help='Creates a mysql database "tennis" with empty tables')

    # Subparser for 'create_db' command
    subparsers.add_parser('create_db', help='Creates a mysql database "tennis" with filled tables')
    args = parser.parse_args()

    # Execute the command based on the provided arguments
    if args.command == 'tournaments':
        print(f"Executing 'tournaments' command for the year {args.year}")
        print("Loading...")
        table = tournaments.run(args.year)
        tournaments.print_data(table)

    elif args.command == 'ranking':
        print(f"Executing 'ranking' command for the year {args.year} with {args.number_of_players} players")
        print("Loading...")
        table = rankings.run(args.number_of_players, args.year)
        rankings.print_data(table)

    elif args.command == 'empty_db':
        print(f"Creating empty database 'tennis'")
        create_sql_file()
        execute_sql_file()

    elif args.command == 'create_db':
        print(f"Creating database 'tennis'")
        print(f"This will take a few minutes...")
        create_sql_file()
        execute_sql_file()
        get_players_info()
        get_tournament_info()

    else:
        print("Invalid command. Supported commands: tournaments, ranking")


if __name__ == "__main__":
    main()
