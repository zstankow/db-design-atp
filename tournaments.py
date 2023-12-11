from tennis_logger import logger
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate


def select_top_player_checkbox(driver, button_selector, dropdown_selector, option_display):
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             button_selector))
    )
    button.click()

    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )

    # Selecting number of display results as "All"
    option_display = WebDriverWait(dropdown_menu, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, option_display))
    )
    option_display.click()


def select_season(driver, display_seasons, year):
    button_year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, display_seasons))
    )
    button_year.click()

    select = Select(button_year)
    select.select_by_value(year)


def select_num_display_results(driver, button_selector, dropdown_selector, option_click):
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             button_selector))
    )
    button.click()

    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )

    option_display = WebDriverWait(dropdown_menu, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, option_click))
    )
    option_display.click()


def get_tournaments_info(driver):
    """
    Fetches tennis player ranking information from a web page and returns tabulated data.

    Args:
        driver (WebDriver): The Selenium WebDriver instance for automated web browsing.

    Returns:
        list: A list containing tabulated player data.
    """
    try:
        display_results_button = "#tournamentsTable-header > div > div > div.actions.btn-group > div:nth-child(2) > button"
        dropdown = "#tournamentsTable-header > div > div > div.actions.btn-group > div.dropdown.btn-group.open > ul"
        option = "All"
        select_num_display_results(driver, display_results_button, dropdown, option)

        display_seasons_button = "fromSeason"
        year = "2023"
        select_season(driver, display_seasons_button, year)

        display_checkbox = "#tournamentsTable-header > div > div > div.actions.btn-group > div:nth-child(3) > button"
        dropdown = "#tournamentsTable-header > div > div > div.actions.btn-group > div:nth-child(3) > ul"
        option = 'input[name="topPlayers"]'
        select_top_player_checkbox(driver, display_checkbox, dropdown, option)

        # Extracts table
        table = driver.find_element_by_id('tournamentsTable')
        time.sleep(1)
        tournament_rows = table.find_elements_by_css_selector('tbody tr')
        logger.info(f"Successfully fetched all rows from table.")

    except Exception as e:
        logger.error(f"{e}: Failed to fetch all rows.")
        driver.quit()
        return []
    return get_tabulated_data(tournament_rows)


def get_tabulated_data(rows):
    """
    Extracts and tabulates player information from a list of player rows.

    Args:
        rows (list): List of Selenium WebElement representing player rows.

    Returns:
        None: Prints the tabulated player information.
    """
    players_info = []
    for row in rows:
        try:
            cells = row.find_elements_by_tag_name('td')
            row_data = {
                'name': cells[0].text,
                'level': cells[1].text,
                'surface': cells[2].text,
                'part': cells[4].text,
                'str': cells[5].text,
                'elo': cells[6].text,
                'winner first': cells[7].text.split()[1],
                'winner last': " ".join(cells[7].text.split()[2:])
            }
            players_info.append([row_data['name'], row_data['level'],
                                row_data['surface'], row_data['part'],
                                row_data['str'], row_data['elo'], row_data['winner first'],
                                row_data['winner last']
                                ])
            logger.info(f"Tournament {row_data['name']} added to list.")
        except Exception as e:
            logger.info(f"{e}: Failed to extract information on tournament.")

    print("\n", tabulate(players_info, headers=[
        "Tournament Name", "Level", "Surface", "Part.", "Str.", "Elo", "Winner First Name", "Winner Last Name"
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
    tournament_url = "https://www.ultimatetennisstatistics.com/tournaments"
    try:
        driver.get(tournament_url)
        logger.info(f"Successfully fetched URL: {tournament_url}")
    except Exception as e:
        logger.error(f"{e}: Failed to fetch URL: {tournament_url}")
        driver.quit()

    get_tournaments_info(driver)
    driver.quit()


if __name__ == "__main__":
    main()