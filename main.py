import rankings
import tournaments
from create_sql_file import create_sql_file
import argparse
import pymysql
import pymysql.cursors
from tabulate import tabulate


def print_tabulated_tournament_data(tournament_info):
    print("\n", tabulate(tournament_info, headers=[
        "Tournament Name", "Level", "Surface", "Part.", "Str.", "Elo", "Winner"
    ], tablefmt="pretty"))


def print_tabulated_players_data(players_info):
    print("\n", tabulate(players_info, headers=[
            "Current Ranking", "Best Ranking", "Name", "Country", "+/- Positions", "+/- Points"
    ], tablefmt="pretty"))


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
    parser_empty_db = subparsers.add_parser('empty_db', help='Creates an mysql database "tennis" with empty tables')
    parser_empty_db.add_argument('user', type=str, help='MySQL user')
    parser_empty_db.add_argument('password', type=str, help='MySQL password')

    # Subparser for 'create_db' command
    parser_db = subparsers.add_parser('create_db', help='Creates an mysql database "tennis" with filled tables')
    parser_db.add_argument('user', type=str, help='MySQL user')
    parser_db.add_argument('password', type=str, help='MySQL password')
    args = parser.parse_args()

    # Execute the command based on the provided arguments
    if args.command == 'tournaments':
        print(f"Executing 'tournaments' command for the year {args.year}")
        print("Loading...")
        table = tournaments.main(args.year)
        print_tabulated_tournament_data(table)

    elif args.command == 'ranking':
        print(f"Executing 'ranking' command for the year {args.year} with {args.number_of_players} players")
        print("Loading...")
        table = rankings.main(args.number_of_players, args.year)
        print_tabulated_players_data(table)

    elif args.command == 'empty_db':
        print(f"Creating empty database 'tennis'")
        create_sql_file()

    elif args.command == 'create_db':
        print(f"Creating database 'tennis'")
        print(f"This will take a few minutes...")
        create_sql_file()
        connection = pymysql.connect(host='localhost', user=args.user, password=args.password)
        cursor = connection.cursor()

        with open('tennis_database.sql', 'r') as file:
            sql_commands = file.read()
            cursor.execute(sql_commands)
            connection.commit()
            # HERE PLACE THE FUNCTION THAT FILLS THE TABLES

    else:
        print("Invalid command. Supported commands: tournaments, ranking")


if __name__ == "__main__":
    main()
