from tennis_logger import logger
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def click_all_checkboxes(dropdown, option):
    option_display = WebDriverWait(dropdown, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, option))
    )
    if not option_display.is_selected():
        option_display.click()


def select_checkboxes(driver):
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

    checkbox_list_str = ["name", "levels", "surfaces", "speeds",
                         "eventCount", "seasons", "playerCount", "participation",
                         "strength", "averageEloRating", "topPlayers"]

    for box in checkbox_list_str:
        option = f'input[name="{box}"]'
        click_all_checkboxes(dropdown_menu, option)


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
        select_checkboxes(driver)

        # Extracts table
        time.sleep(2)
        table = driver.find_element(By.ID, 'tournamentsTable')
        time.sleep(2)
        tournament_rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
        logger.info(f"Successfully fetched all rows from table.")

    except Exception as e:
        logger.error(f"{e}: Failed to fetch all rows.")
        driver.quit()
        return []
    return get_tabulated_data(tournament_rows)


def get_tabulated_data(rows):
    tournament_info = []
    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = {
                'name': cells[0].text,
                'level': cells[1].text,
                'surface': cells[2].text,
                'part': cells[7].text,
                'str': cells[8].text,
                'elo': cells[9].text,
                'winner': " ".join(cells[10].text.split()[1:])
            }
            tournament_info.append([row_data['name'], row_data['level'],
                                    row_data['surface'], row_data['part'],
                                    row_data['str'], row_data['elo'], row_data['winner']
                                    ])
            logger.info(f"Tournament {row_data['name']} added to list.")
        except Exception as e:
            logger.info(f"{e}: Failed to extract information on tournament.")
    print(tournament_info)
    return tournament_info


def call_driver():
    driver = webdriver.Chrome()
    tournament_url = "https://www.ultimatetennisstatistics.com/tournaments"
    try:
        driver.get(tournament_url)
        logger.info(f"Successfully fetched URL: {tournament_url}")
    except Exception as e:
        logger.error(f"{e}: Failed to fetch URL: {tournament_url}")
        driver.quit()
    return driver


def main(year='2023'):
    driver = call_driver()
    table = get_tournaments_info(driver, year)
    driver.quit()
    return table
