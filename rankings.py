from tennis_logger import logger
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate


def get_players_info(driver):
    """
    Fetches tennis player ranking information from a web page and returns tabulated data.

    Args:
        driver (WebDriver): The Selenium WebDriver instance for automated web browsing.
        display_num (str): The desired number of displayed results.

    Returns:
        list: A list containing tabulated player data.
    """
    try:
        # Clicking button responsible for number of display results.
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "#rankingsTable-header > div > div > div.actions.btn-group > div:nth-child(2) > button"))
        )
        button.click()

        # Locating the dropdown menu options
        dropdown_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#rankingsTable-header > div > div > "
                                                             "div.actions.btn-group > div.dropdown.btn-group.open "
                                                             "> ul"))
        )

        # Selecting number of display results as 100
        option_display = WebDriverWait(dropdown_menu, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "All"))
        )
        option_display.click()

        # Extracts table
        time.sleep(2)
        player_rows = driver.find_elements_by_css_selector('tbody tr')
        logger.info(f"Successfully fetched all rows from table.")

    except Exception as e:
        logger.error(f"{e}: Failed to fetch all rows.")
        driver.quit()
        return []
    return get_tabulated_data(player_rows)


def get_tabulated_data(player_rows):
    """
    Extracts and tabulates player information from a list of player rows.

    Args:
        player_rows (list): List of Selenium WebElement representing player rows.

    Returns:
        None: Prints the tabulated player information.
    """
    players_info = []
    for row in player_rows:
        try:
            cells = row.find_elements_by_tag_name('td')
            row_data = {
                'ranking': cells[0].text.split(" ")[0],
                'best rank': cells[1].text,
                'country': cells[2].text,
                'name': cells[3].text,
                '+/- position': cells[4].text,
                '+/- points': cells[5].text
            }
            players_info.append([row_data['ranking'], row_data['best rank'],
                                row_data['name'], row_data['country'],
                                row_data['+/- position'], row_data['+/- points']])
            logger.info(f"Player {row_data['name']} added to list.")
        except Exception as e:
            logger.info(f"{e}: Failed to extract information on player.")

    print("\n", tabulate(players_info, headers=[
        "Current Ranking", "Best Ranking", "Name", "Country", "+/- Positions", "+/- Points"
                                ], tablefmt="pretty"))


def verify_input(num):
    """
    Validates user input for the number of top tennis players' rankings to display.

    Args:
        num (str): The user-provided input for the number of players.

    Returns:
        str: The valid input for the number of top tennis players' rankings.
    """
    while True:
        if num not in ['20', '50', '100']:
            print("Sorry, that is not a valid input.")
            num = input("Please select the number of top tennis players' rankings you would "
                        "like to display: 20, 50, or 100: ")
        else:
            print("Just a moment...\n")
            return num


# def menu():
#     """
#     Displays the ATP Rankings menu and retrieves user input for the number of players.
#
#     Returns:
#         str: The valid input for the number of top tennis players' rankings.
#     """
#     print("\n *** ATP RANKINGS *** \n")
#     num_display = verify_input(input("Please select the number of top tennis players' rankings you would "
#                                      "like to display: 20, 50, or 100: "))
#     return num_display


def main():

    driver = webdriver.Chrome()
    player_ranking_url = "https://www.ultimatetennisstatistics.com/rankingsTable"
    try:
        driver.get(player_ranking_url)
        logger.info(f"Successfully fetched URL: {player_ranking_url}")
    except Exception as e:
        logger.error(f"{e}: Failed to fetch URL: {player_ranking_url}")
        driver.quit()

    get_players_info(driver)
    driver.quit()


if __name__ == '__main__':
    main()
