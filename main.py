import rankings
import tournaments
import argparse

def verify_input(user_input):
    """
    Validates user input for ATP Rankings menu options.

    Args:
        user_input (str): The user-provided input for the menu option.

    Returns:
        str: The valid input for the ATP Rankings menu.
    """
    while True:
        if user_input not in ['head2head', 'ranking', '-h']:
            user_input = input("Invalid input: Please type either 'head2head' or 'ranking' or type '-h' for help. ")
        elif user_input == '-h':
            print("head2head: type the name of 2 players and see their stats side by side!\n"
                  "ranking: displays a list of top players and stats")
            user_input = input("Type either 'head2head' or 'ranking' or type '-h' for help. ")
        else:
            return user_input


def main():

    user = verify_input(input("Type one of two options: 'head2head' or 'ranking': "))
    if user == 'head2head':
        tournaments.main()
    if user == 'ranking':
        rankings.main()

##################################
    parser = argparse.ArgumentParser(description='scrape_all top_players_start_with_a')
        parser.add_argument('-w', action='store_true',
                            help='Print "hello there!" message')
        parser.add_argument("operation", type=str,
                            help='Type an operation from the following list: add, subtract, multiply, divide')
        parser.add_argument("first_number", type=float,
                            help='Type an integer value')
        parser.add_argument("second_number", type=float,
                            help='Type an integer value')

        input_args = parser.parse_args()

        if input_args.w:
            print("Hello there!")

        result = operator(input_args.first_number,
                          input_args.second_number, input_args.operation)
        print(result)


if __name__ == "__main__":
    main()
