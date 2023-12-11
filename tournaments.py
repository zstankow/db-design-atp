from tennis_logger import logger
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate


def select_top_player_checkbox(driver):
    checkbox_button = "#tournamentsTable-header > div > div > div.actions.btn-group > div:nth-child(3) > button"
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             checkbox_button))
    )
    button.click()

    dropdown_selector = "#tournamentsTable-header > div > div > div.actions.btn-group > div:nth-child(3) > ul"
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )

    option = 'input[name="topPlayers"]'
    option_display = WebDriverWait(dropdown_menu, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, option))
    )
    option_display.click()


def select_season(driver, year):
    seasons_button = "fromSeason"
    button_year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, seasons_button))
    )
    button_year.click()

    select = Select(button_year)
    select.select_by_value(year)


def select_num_display_results(driver, num="All"):
    button_selector = "#tournamentsTable-header > div > div > div.actions.btn-group > div:nth-child(2) > button"
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             button_selector))
    )
    button.click()

    dropdown_selector = "#tournamentsTable-header > div > div > div.actions.btn-group > div.dropdown.btn-group.open > ul"
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )

    option_display = WebDriverWait(dropdown_menu, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, num))
    )
    option_display.click()


def get_tournaments_info(driver, year='2023'):
    try:
        select_num_display_results(driver)
        select_season(driver, year)
        select_top_player_checkbox(driver)

        # Extracts table
        time.sleep(2)
        table = driver.find_element_by_id('tournamentsTable')
        time.sleep(2)
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
                'winner': " ".join(cells[7].text.split()[1:])
            }
            players_info.append([row_data['name'], row_data['level'],
                                row_data['surface'], row_data['part'],
                                row_data['str'], row_data['elo'], row_data['winner']
                                ])
            logger.info(f"Tournament {row_data['name']} added to list.")
        except Exception as e:
            logger.info(f"{e}: Failed to extract information on tournament.")

    print("\n", tabulate(players_info, headers=[
        "Tournament Name", "Level", "Surface", "Part.", "Str.", "Elo", "Winner"
                                ], tablefmt="pretty"))


def main(year='2023'):

    driver = webdriver.Chrome()
    tournament_url = "https://www.ultimatetennisstatistics.com/tournaments"
    try:
        driver.get(tournament_url)
        logger.info(f"Successfully fetched URL: {tournament_url}")
    except Exception as e:
        logger.error(f"{e}: Failed to fetch URL: {tournament_url}")
        driver.quit()

    get_tournaments_info(driver, year)
    driver.quit()


# if __name__ == '__main__':
#     main('2015')
