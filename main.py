import rankings
import tournaments
import argparse

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

    args = parser.parse_args()

    # Execute the command based on the provided arguments
    if args.command == 'tournaments':
        print(f"Executing 'tournaments' command for the year {args.year}")
        print("Loading...")
        tournaments.main(args.year)
    elif args.command == 'ranking':
        print(f"Executing 'ranking' command for the year {args.year} with {args.number_of_players} players")
        print("Loading...")
        rankings.main(args.number_of_players, args.year)
    else:
        print("Invalid command. Supported commands: tournaments, ranking")


if __name__ == "__main__":
    main()


