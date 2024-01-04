from tennis_logger import logger
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
import json
import pandas as pd
import numpy as np
import re

with open('config.json', 'r') as file:
    conf = json.load(file)


def select_num_display_results(driver, header, tail_button, tail_dropdown, num):
    """
    Changes number of display results from default value to num
    """
    button_selector = header + tail_button
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             button_selector))
    )
    button.click()
    time.sleep(0.2)

    dropdown_selector = header + tail_dropdown
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )
    time.sleep(0.2)

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


def get_players_info(driver, num="200", year='2023'):
    """
    Retrieves web-scraped data on player rankings for selected year.
    Returns dataframe of player ranking data
    """
    try:
        # Clicking button responsible for number of display results.
        select_num_display_results(driver, header=conf["RANKING_TABLE_HEADER"],
                                   tail_button=conf["NUM_DISPLAY_BUTTON"], tail_dropdown=conf["NUM_DISPLAY_DROPDOWN"],
                                   num="All")
        select_year(driver, year)

        # Extracts table
        time.sleep(2)
        player_rows = driver.find_elements(By.CSS_SELECTOR, conf["ROWS"])
        logger.info(f"Successfully fetched all rows from table.")

    except Exception as e:
        logger.error(f"{e}: Failed to fetch all rows.")
        driver.quit()
        return []
    return get_tabulated_ranking_data(player_rows, num)


def get_tabulated_ranking_data(player_rows, num):
    """
    Receives list of web-scraped player ranking data and creates a dataframe called player_info.
    Returns dataframe
    """
    players_info = pd.DataFrame(columns=["Current Ranking", "Best Ranking", "Name",
                                         "Country", "+/- Positions", "+/- Points"])
    for i, row in enumerate(player_rows):
        try:
            if i < int(num):
                cells = row.find_elements(By.TAG_NAME, conf["CELLS"])
                row_data = {
                    "Current Ranking": cells[0].text.split(" ")[0],
                    "Best Ranking": cells[1].text,
                    "Country": cells[2].text,
                    "Name": cells[3].text,
                    "+/- Positions": cells[4].text if cells[4].text != '-' else np.nan,
                    "+/- Points": cells[5].text
                }
                row_data_df = pd.DataFrame([row_data])
                players_info = pd.concat([players_info, row_data_df], ignore_index=True)
                logger.info(f"Player {row_data['Name']} added to list.")
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


def select_checkboxes(driver, header, tail_button, tail_dropdown, checkbox_list):
    """
    Selects all checkboxes on tournament webpage to ensure all columns are collected from table.
    """
    checkbox_button = header + tail_button
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             checkbox_button))
    )
    button.click()
    time.sleep(0.5)
    dropdown_selector = header + tail_dropdown
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             dropdown_selector))
    )

    for box in checkbox_list:
        option = f'input[name="{box}"]'
        click_all_checkboxes(dropdown_menu, option)
        time.sleep(0.5)


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
    time.sleep(0.5)

    button_year = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, conf["TO_SEASON"]))
    )
    button_year.click()
    time.sleep(0.5)
    select = Select(button_year)
    select.select_by_value(year)


def get_events_urls(rows):
    """
    Receives rows of a table containing html with links.
    Returns the links extracted from the html.
    """
    urls = []
    for row in rows:
        anchor = WebDriverWait(row, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        urls.append(anchor.get_attribute('href'))
    return urls


def get_events_info(driver, year='2014'):
    """
    Retrieves table data on events from years 2023 to 2014.
    Returns list of the rows of the data.
    """
    # Change number of display results to "All", tournament season to 2014
    select_num_display_results(driver, conf["TOURNAMENTS_TABLE_HEADER"],
                               conf["NUM_DISPLAY_BUTTON"], conf["NUM_DISPLAY_DROPDOWN"],
                               "All")
    select_season(driver, year)
    time.sleep(2)
    table_rows = driver.find_elements(By.CSS_SELECTOR, conf["ROWS"])
    events_urls = get_events_urls(table_rows)
    driver.quit()

    event_df = pd.DataFrame(columns=["Date", "Name", "Winner", "Finalist", "Score"])
    for url in events_urls:
        try:
            driver = call_driver(url)
            driver.execute_script("window.scrollTo(0, 400)")
            select_num_display_results(driver, conf["EVENTS_TABLE_HEADER"], conf["EVENTS_NUM_DISPLAY_BUTTON"],
                                       conf["EVENTS_NUM_DISPLAY_DROPDOWN"], "All")
            checkbox_list_str = conf["CHECK_BOX_LIST_EVENTS"]
            select_checkboxes(driver, conf["EVENTS_TABLE_HEADER"], conf["EVENTS_CHECKBOX_BUTTON"],
                              conf["EVENTS_CHECKBOX_DROPDOWN"], checkbox_list_str)
            time.sleep(2)
            table = driver.find_element(By.ID, 'tournamentEventsTable')
            time.sleep(2)
            event_rows = table.find_elements(By.CSS_SELECTOR, conf["ROWS"])
            event_info = get_event_tabulated_data(event_rows)
            logger.info(f"Successfully fetched all rows from table at url {url}.")
            event_df = pd.concat([event_df, event_info], ignore_index=True)
            logger.info(f"Added event information at {url} to the dataframe event_df.")
            driver.quit()

        except Exception as e:
            logger.info(f"Unable to extract events at {url}.")
            driver.quit()
            return pd.DataFrame()
    return event_df


def is_date_after(date, year=2014):
    if date.year >= year:
        return True
    return False


def get_event_tabulated_data(rows):
    """
    Receives a list of rows from the event data and creates a dataframe called event_info.
    Returns a dataframe.
    """
    event_info = pd.DataFrame(columns=["Date", "Name", "Winner", "Finalist", "Score"])
    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, conf["CELLS"])
            pattern = re.compile(r'(\w+\s\w+)\s\(\d+\) d\. (\w+\s\w+)\s\(\d+\) (.+)$')
            text = cells[9].text
            match = pattern.match(text)
            row_data = {
                "Date": datetime.strptime(cells[0].text, '%d-%m-%Y'),
                "Name": cells[1].text,
                "Winner": match.group(1),
                "Finalist": match.group(2),
                "Score": match.group(3),
            }
            is_after = is_date_after(row_data["Date"])
            if is_after:
                row_data_df = pd.DataFrame([row_data])
                event_info = pd.concat([event_info, row_data_df], ignore_index=True)
                logger.info(f"Event {row_data['Name']} added to list.")
            else:
                return event_info
        except Exception as e:
            logger.info(f"{e}: Failed to extract information on event.")
    return event_info


def get_tournaments_info(driver, year='2023'):
    """
    Retrieves table data on tournaments for a specified year.
    Returns list of the rows of the data.
    """
    try:
        select_num_display_results(driver, conf["TOURNAMENTS_TABLE_HEADER"],
                                   conf["NUM_DISPLAY_BUTTON"], conf["NUM_DISPLAY_DROPDOWN"],"All")
        select_season(driver, year)
        checkbox_list_str = conf["CHECK_BOX_LIST_TOURNAMENTS"]
        select_checkboxes(driver, conf["TOURNAMENTS_TABLE_HEADER"], conf["CHECKBOX_BUTTON"],
                          conf["CHECKBOX_DROPDOWN"], checkbox_list_str)

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
    Receives a list of rows from the tournament data and creates a dataframe called tournament_info.
    Returns a dataframe.
    """
    tournament_info = pd.DataFrame(columns=["Name", "Level", "Surface", "Seasons", "Part", "Str.", "Elo.", "Winner"])
    for row in rows:
        try:
            cells = row.find_elements(By.TAG_NAME, conf["CELLS"])
            row_data = {
                "Name": cells[0].text,
                "Level": cells[1].text,
                "Surface": cells[2].text,
                "Seasons": cells[5].text,
                "Part": cells[7].text,
                "Str.": cells[8].text,
                "Elo.": cells[9].text,
                "Winner": " ".join(cells[10].text.split()[1:])
            }
            row_data_df = pd.DataFrame([row_data])
            tournament_info = pd.concat([tournament_info, row_data_df], ignore_index=True)
            logger.info(f"Tournament {row_data['Name']} added to list.")
        except Exception as e:
            logger.info(f"{e}: Failed to extract information on tournament.")
    return tournament_info


def call_driver(url):
    """
    Calls the Chrome webdriver.
    Returns the driver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures the browser runs in headless mode
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED on Linux
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)

    try:
        driver.get(url)
        logger.info(f"Successfully fetched URL: {url}")
    except Exception as e:
        logger.error(f"{e}: Failed to fetch URL: {url}")
        driver.quit()
    return driver


def print_data(data):
    """
    Receives a dataframe of tournament data and prints the data.
    """
    print(tabulate(data, headers='keys', tablefmt='psql'))


def scrape_tournaments(year='2023'):
    driver = call_driver(conf["TOURNAMENTS_URL"])
    df = get_tournaments_info(driver, year)
    driver.quit()
    return df


def scrape_rankings(number_of_players="200", year='2023'):
    driver = call_driver(conf["RANKING_URL"])
    df = get_players_info(driver, number_of_players, year)
    driver.quit()
    return df


def scrape_events(year='2014'):
    driver = call_driver(conf["TOURNAMENTS_URL"])
    get_events_info(driver, year)
    driver.quit()
