from tennis_logger import logger
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
import json

with open('config.json', 'r') as file:
    conf = json.load(file)


def select_num_display_results(driver, header, num):
    """
    Changes number of display results from default value to num
    """
    button_selector = header + conf["NUM_DISPLAY_BUTTON"]
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             button_selector))
    )
    button.click()

    dropdown_selector = header + conf["DROPDOWN_SELECTOR_1"]
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )

    option_display = WebDriverWait(dropdown_menu, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, num))
    )
    option_display.click()


def select_year(driver, year='2023'):
    """
    Changes year of display results from default value to value of year parameter.
    """
    button_year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, conf["SEASONS_BUTTON"]))
    )
    button_year.click()
    time.sleep(2)
    select = Select(button_year)
    select.select_by_value(year)


def get_players_info(driver, year='2023'):
    """
    Retrieves web-scraped data on player rankings for selected year.
    Returns list of data
    """
    try:
        # Clicking button responsible for number of display results.
        select_num_display_results(driver, conf["RANKING_TABLE_HEADER"], "All")
        select_year(driver, year)

        # Extracts table
        time.sleep(2)
        player_rows = driver.find_elements(By.CSS_SELECTOR, conf["ROWS"])
        logger.info(f"Successfully fetched all rows from table.")

    except Exception as e:
        logger.error(f"{e}: Failed to fetch all rows.")
        driver.quit()
        return []
    return player_rows


def get_tabulated_ranking_data(player_rows, num):
    """
    Receives list of web-scraped player ranking data and tabulates it into a list of lists.
    Returns list of data
    """
    players_info = []
    for i, row in enumerate(player_rows):
        try:
            if i < int(num):
                cells = row.find_elements(By.TAG_NAME, conf["CELLS"])
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
            else:
                break
        except Exception as e:
            logger.info(f"{e}: Failed to extract information on player.")
    return players_info


def click_all_checkboxes(dropdown, option):
    """
    Clicks checkbox to display column specified by the checkbox on tournament webpage.
    """
    option_display = WebDriverWait(dropdown, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, option))
    )
    if not option_display.is_selected():
        option_display.click()


def select_checkboxes(driver):
    """
    Selects all checkboxes on tournament webpage to ensure all columns are collected from table.
    """
    checkbox_button = conf["TOURNAMENTS_TABLE_HEADER"] + conf["CHECKBOX_BUTTON"]
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             checkbox_button))
    )
    button.click()

    dropdown_selector = conf["TOURNAMENTS_TABLE_HEADER"] + conf["DROPDOWN_SELECTOR_2"]
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )

    checkbox_list_str = ["name", "levels", "surfaces", "speeds",
                         "eventCount", "seasons", "playerCount", "participation",
                         "strength", "averageEloRating", "topPlayers"]

    for box in checkbox_list_str:
        option = f'input[name="{box}"]'
        click_all_checkboxes(dropdown_menu, option)


def select_season(driver, year):
    """
    Selects specified year in dropdown menu on tournament webpage.
    """
    button_year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, conf["FROM_SEASON"]))
    )
    button_year.click()

    select = Select(button_year)
    select.select_by_value(year)

    button_year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, conf["TO_SEASON"]))
    )
    button_year.click()
    select = Select(button_year)
    select.select_by_value(year)


def get_tournaments_info(driver, year='2023'):
    """
    Retrieves table data on tournaments for a specified year.
    Returns list of the rows of the data.
    """
    try:
        select_num_display_results(driver, header=conf["TOURNAMENTS_TABLE_HEADER"], num="All")
        select_season(driver, year)
        select_checkboxes(driver)

        # Extracts table
        time.sleep(2)
        table = driver.find_element(By.ID, 'tournamentsTable')
        time.sleep(2)
        tournament_rows = table.find_elements(By.CSS_SELECTOR, conf["ROWS"])
        logger.info(f"Successfully fetched all rows from table.")

    except Exception as e:
        logger.error(f"{e}: Failed to fetch all rows.")
        driver.quit()
        return []
    return get_tournament_tabulated_data(tournament_rows)


def get_tournament_tabulated_data(rows):
    """
    Receives a list of rows from the tournament data and extracts the table values.
    Returns a list of the extracted values
    """
    tournament_info = []
    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, conf["CELLS"])
            row_data = {
                'name': cells[0].text,
                'level': cells[1].text,
                'surface': cells[2].text,
                'seasons': cells[5].text,
                'part': cells[7].text,
                'str': cells[8].text,
                'elo': cells[9].text,
                'winner': " ".join(cells[10].text.split()[1:])
            }
            tournament_info.append([row_data['name'], row_data['level'],
                                    row_data['surface'], row_data['seasons'], row_data['part'],
                                    row_data['str'], row_data['elo'], row_data['winner']
                                    ])
            logger.info(f"Tournament {row_data['name']} added to list.")
        except Exception as e:
            logger.info(f"{e}: Failed to extract information on tournament.")
    return tournament_info


def call_driver(url):
    """
    Calls the Chrome webdriver.
    Returns the driver.
    """
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        logger.info(f"Successfully fetched URL: {url}")
    except Exception as e:
        logger.error(f"{e}: Failed to fetch URL: {url}")
        driver.quit()
    return driver


def print_tournament_data(tournament_info):
    """
        Receives a list of lists of player ranking data and prints the data.
    """
    print("\n", tabulate(tournament_info, headers=[
        "Tournament Name", "Level", "Surface", "Season", "Part.", "Str.", "Elo.", "Winner"
    ], tablefmt="pretty"))


def print_ranking_data(players_info):
    """
    Receives a list of lists of player ranking data and prints the data.
    """
    print("\n", tabulate(players_info, headers=[
            "Current Ranking", "Best Ranking", "Name", "Country", "+/- Positions", "+/- Points"
    ], tablefmt="pretty"))


def run_tournaments(year='2023'):
    driver = call_driver(conf["TOURNAMENTS_URL"])
    table = get_tournaments_info(driver, year)
    driver.quit()
    return table


def run_rankings(number_of_players="200", year='2023'):
    driver = call_driver(conf["RANKING_URL"])
    table = get_tabulated_ranking_data(get_players_info(driver, year), number_of_players)
    driver.quit()
    return table
