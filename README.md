# __Webscraping and Database Design__
## __Tennis Tournaments and Player Rankings__

This Python script retrieves ATP tennis player rankings from the 
[Ultimate Tennis Statistics website](https://www.ultimatetennisstatistics.com/) and has three possible functionalities:

1. To run commands from the CLI that either webscrapes the tournaments or player rankings from a user-specified year (for player rankings, number of top players is also user-specified).
2. To create an empty database with the different tables.
3. To create a relational DB that contains player informations, tournaments, and finals of these tournaments from the past 10 years (from 2014 and onwards). 

Initially, our approach involved using the `requests` and `BeautifulSoup` libraries to parse data from tables. However, we quickly realized that the target website employs dynamic content, prompting a switch to the more suitable `selenium` library.

## Common Issues and Solution

During the debugging phase, we encountered a common issue where the script could extract table data successfully, but when executed, the driver closed before parsing the HTML. To address this, we employed a combination of `time.sleep()`, `WebDriverWait`, and `expected_conditions` modules.

### Example from rankings.py Script

In one scenario, the script involves interacting with a dropdown menu to adjust the number of displayed results. A frequent problem was the driver closing immediately after making the selection, preventing sufficient time for table extraction.

```
# After opening dropdown menu, clicks on chosen number of display results
option_display = WebDriverWait(dropdown_menu, 10).until( 
    EC.element_to_be_clickable((By.LINK_TEXT, display_num))
)
option_display.click()
```
By utilizing the `WebDriverWait` module, we ensure that the driver loads the dropdown menu before closing, allowing time for itself to click on the chosen option.
```
# Adding a 1-second sleep to ensure the driver does not close too quickly
time.sleep(1)

# Extracting player rows after the dropdown selection
player_rows = driver.find_elements_by_css_selector('tbody tr')
```
By incorporating a brief `time.sleep(1)` pause, we ensure that the driver doesn't close prematurely, allowing adequate time for the table extraction process to complete successfully.

## Dependencies
- __selenium__

  `pip install selenium`

- __WebDriver__: make sure you have the Chrome WebDriver executable installed and available
  in your system path. Ensure that the version is compatible with you chrome browser. You can download the driver [here](https://chromedriver.chromium.org/downloads).

- other dependencies can be found in the __requirements.txt__ file

## Usage
1. Clone the repository or download the following scripts:
- `main.py`
- `data_collector.py.py`
- `data_collector.py`
- `tennis_sql_schema.sql`

2. Run the script in your cmd:
   1. to print ranking of a certain year :  python main.py ranking year number_of_players 
   2. to print tournaments of a certain year : python main.py tournaments year
   3. to create empty db : python main.py empty_db
   4. to create a full db : python main.py create_db
   
3. The script will fetch the data from the Ultimate Tennis Statistics website and display the results.

## Logging
The script logs relevant information and errors to a file named `tennis.log`

### Authors
Zoe Stankowski: ([LinkedIn](https://www.linkedin.com/in/zoe-stankowska/)) &
Nathan Szpilman: ([LinkedIn](https://www.linkedin.com/in/nathan-szpilman-3816b31b6/))
