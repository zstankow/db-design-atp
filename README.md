Authors: Zoe Stankowski & Nathan Szpilman

## __Ultimate ATP Tennis Statistics__
This Python script retrieves ATP tennis stats from the 
[Ultimate Tennis Statistics website](https://www.ultimatetennisstatistics.com/): the ultimate men's tennis statistics destination for the die-hard tennis fans!
Be it latest or historical results, in-match statistics, records or all-time greats comparisons, Elo ratings or tournament forecasts, you will find it there.

## The data scraped:
- Tournaments
- Players
- Events
- Posts

All the information is gathered to better understand the stats of the top players and most recent events.

## Objectives:

- To successfully scrape relevant data from the website.
- Create a large DB of information about tennis players and past events.

## Methods and Used Libraries:

The code is divided into a few main stages:
1. parse the user arguments and filters using `argparse` library.
2. Create the DB "tennis".
3. Aquiring the data within the website's tables by webscraping using `selenium`.
4. Inserting the data into the DB created in stage two.

## User Arguments:

Four possible arguments are available:
- create_db - scrapes all the relevant data from the years 2014 and onwards
- empty_db - creates empty DB tennis with the relevant tables
- ranking - prints the top x players from the year y
- tournaments - prints all the tournaments from the year y

For example:
```
python main.py ranking 2014 73
```
will print the top 73 players from the year 2014

## Dependencies
- __selenium__

    `pip install selenium`
- __pymysql__
  
    `pip install pymysql`
- __json__

    `pip install json`

- __WebDriver__: make sure you have the Chrome WebDriver executable installed and available
  in your system path. Ensure that the version is compatible with you chrome browser. You can download the driver [here](https://chromedriver.chromium.org/downloads).

- other dependencies can be found in the __requirements.txt__ file

## Database Structure and Features

![image](https://github.com/zstankow/db-design-atp/assets/150588332/9e9f1ab3-0368-4c0d-b3a4-1fb77de797d6)

players: 
  - player_id [int] - primary key, autogenerated
  - name [varchar] - name of player
  - best_rank [int] - best rank of player
  - country_id [int] - foreign key, nationality of player
  
tournaments:
  - tournament_id [int] - primary key, autogenerated
  - name [varchar] - name of tournament
  - year [int] - year of tournament
  - level [int] - level of tournament 
  - surface [varchar] - type of court surface
  - no_events [int] - number of events in tournament
  - participation_perc [float] - percent of best players who participated
  - strength [int] - weighted sum of participating players strengths
  - avg_elo [int] - average strength of participating players

countries:
  - country_id [int] - primary key, autogenerated
  - name [varchar] - name of country

events:
  - event_id [int] - primary key, autogenerated
  - name [varchar] - name of event
  - tournament_id - foreign key from tournament_id
  - date [date] - date of event
  - winner_id [int] - foreign key from players_id
  - finalist_id [int] - foreign key from players_id
  - score [varchar] - score of final event

posts:
  - post_id [int] - primary key, autogenerated
  - player_id [int] - foreign key from players_id
  - account_name [varchar] - instagram account username of player
  - text [varchar] - text of post
  - likes [int] - number of likes on the post
  - comments [int] - number of comments on the post
  - url [varchar] - url of post


## Running the program

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

## Usage
1. Clone the repository or download the following scripts:
- `main.py`
- `data_collector.py`
- `webscraper.py`
- `tennis_logger.py`
- `config.json`
- `tennis_sql_schema.sql`
- `insta_api.py`

2. Follow requirements.txt installations
3. Before running the script, type your MySQL user and password into the config.json file:
   "MYSQL_USER": "your_user"
   "MYSQL_PASSWORD": "your_password"
4. Run the script in your cmd:
   
    `python main.py`
   
Type `-h` for help in the command arguments decribed in the 'User Arguments' section.

## Logging
The script logs relevant information and errors to a file named `tennis.log`

### Authors
Zoe Stankowski: ([LinkedIn](https://www.linkedin.com/in/zoe-stankowska/)) ([Github](https://github.com/zstankow)) &
Nathan Szpilman: ([LinkedIn](https://www.linkedin.com/in/nathan-szpilman-3816b31b6/)) ([Github](https://github.com/nathszpil))
