import argparse
import json
from tennis_logger import logger
from data_collector import add_players_info, add_tournament_info
import webscraper
import pymysql

# Load json file data
with open('config.json', 'r') as file:
    conf = json.load(file)


def execute_sql_file():
    """
    Executes commands within .sql file.
    Returns None
    """
    connection = pymysql.connect(
        host="localhost",
        user=conf["USER"],
        password=conf["PASSWORD"]
    )
    with connection.cursor() as cursor:
        try:
            with open(conf["DB_COMMANDS_FILE"], 'r') as file:
                sql_commands = file.read()
                # Split SQL commands by semicolon
                commands = sql_commands.split(';')
                for command in commands:
                    # Skip empty commands
                    if command.strip() != '':
                        cursor.execute(command)
            connection.commit()
            logger.info(f'Successfully executed {conf["DB_COMMANDS_FILE"]} file commands.')
        except Exception as e:
            logger.error(f'{e}: Error in executing {conf["DB_COMMANDS_FILE"]} file commands.')
        finally:
            connection.close()


def parse():
    """
    Parses arguments from command line.
    Returns args.
    """
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
    return args


def main():
    args = parse()
    logger.info(f'Args input: {args}')

    # Execute the command based on the provided arguments
    if args.command == 'tournaments':
        print(f"Executing 'tournaments' command for the year {args.year}")
        print("Loading...")
        table = webscraper.scrape_tournaments(args.year)
        webscraper.print_data(table)

    elif args.command == 'ranking':
        print(f"Executing 'ranking' command for the year {args.year} with {args.number_of_players} players")
        print("Loading...")
        table = webscraper.scrape_rankings(args.number_of_players, args.year)
        webscraper.print_data(table)

    elif args.command == 'empty_db':
        print(f"Creating empty database 'tennis'")
        execute_sql_file()
        print(f"Database 'tennis' created.")

    elif args.command == 'create_db':
        print(f"Creating database 'tennis'")
        execute_sql_file()
        print(f"Database 'tennis' created.")
        print(f"Collecting data... This will take a few minutes...")
        add_tournament_info()
        add_players_info()

    else:
        print("Invalid command. Supported commands: tournaments, ranking, empty_db, create_db.")


if __name__ == "__main__":
    main()
