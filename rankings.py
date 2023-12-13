from tennis_logger import logger
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
import tournaments


def select_num_display_results(driver):
    button_selector = "#rankingsTable-header > div > div > div.actions.btn-group > div:nth-child(2) > button"
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             button_selector))
    )
    button.click()

    dropdown_selector = "#rankingsTable-header > div > div > div.actions.btn-group > div.dropdown.btn-group.open > ul"
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )

    option_display = WebDriverWait(dropdown_menu, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "All"))
    )
    option_display.click()


def select_year(driver, year='2023'):
    seasons_button = "season"
    button_year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, seasons_button))
    )
    button_year.click()

    time.sleep(2)
    select = Select(button_year)
    select.select_by_value(year)


def get_players_info(driver, year='2023'):
    try:
        # Clicking button responsible for number of display results.
        select_num_display_results(driver)
        select_year(driver, year)

        # Extracts table
        time.sleep(2)
        player_rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        logger.info(f"Successfully fetched all rows from table.")

    except Exception as e:
        logger.error(f"{e}: Failed to fetch all rows.")
        driver.quit()
        return []
    return player_rows


def get_tabulated_data(player_rows, num):
    players_info = []
    for i, row in enumerate(player_rows):
        try:
            if i < int(num):
                cells = row.find_elements(By.TAG_NAME, 'td')
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

    print("\n", tabulate(players_info, headers=[
        "Current Ranking", "Best Ranking", "Name", "Country", "+/- Positions", "+/- Points"
    ], tablefmt="pretty"))


def main(number_of_players, year='2023'):
    driver = webdriver.Chrome()
    player_ranking_url = "https://www.ultimatetennisstatistics.com/rankingsTable"
    try:
        driver.get(player_ranking_url)
        logger.info(f"Successfully fetched URL: {player_ranking_url}")
    except Exception as e:
        logger.error(f"{e}: Failed to fetch URL: {player_ranking_url}")
        driver.quit()

    get_tabulated_data(get_players_info(driver, year), number_of_players)
    driver.quit()


if __name__ == '__main__':
    main('22', '2012')
