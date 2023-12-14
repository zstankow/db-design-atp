import pymysql

example_info = [['Australian Open', 'Grand Slam', 'Hard', '88.5%', '2926', '2050', 'Novak Djokovic'],
                ['Roland Garros', 'Grand Slam', 'Clay', '90.3%', '2857', '2037', 'Novak Djokovic'],
                ['US Open', 'Grand Slam', 'Hard', '95.0%', '2883', '2042', 'Novak Djokovic'],
                ['Wimbledon', 'Grand Slam', 'Grass', '92.5%', '2853', '2036', 'Carlos Alcaraz Garfia'],
                ['Tour Finals', 'Tour Finals', 'Hard', '98.3%', '1069', '2229', 'Novak Djokovic'],
                ['Cincinnati Masters', 'Masters', 'Hard', '88.7%', '2096', '2069', 'Novak Djokovic'],
                ['Indian Wells Masters', 'Masters', 'Hard', '79.0%', '2184', '2013', 'Carlos Alcaraz Garfia'],
                ['Madrid Masters', 'Masters', 'Clay', '80.5%', '2149', '2026', 'Carlos Alcaraz Garfia'],
                ['Miami Masters', 'Masters', 'Hard', '83.0%', '2170', '2031', 'Daniil Medvedev'],
                ['Monte-Carlo Masters', 'Masters', 'Clay', '75.9%', '2035', '2053', 'Andrey Rublev'],
                ['Paris Masters', 'Masters', 'Hard', '94.8%', '2109', '2073', 'Novak Djokovic'],
                ['Rome Masters', 'Masters', 'Clay', '87.2%', '2231', '2046', 'Daniil Medvedev'],
                ['Shanghai Masters', 'Masters', 'Hard', '88.3%', '2140', '2024', 'Hubert Hurkacz'],
                ['Toronto Masters', 'Masters', 'Hard', '81.0%', '2012', '2046', 'Jannik Sinner'],
                ['Acapulco', 'ATP 500', 'Hard', '33.9%', '1326', '1930', 'Alex De Minaur'],
                ['Barcelona', 'ATP 500', 'Clay', '49.1%', '1639', '1961', 'Carlos Alcaraz Garfia'],
                ['Basel', 'ATP 500', 'Hard', '45.9%', '1402', '1954', 'Felix Auger Aliassime'],
                ['Beijing', 'ATP 500', 'Hard', '74.1%', '1701', '2051', 'Jannik Sinner'],
                ['Dubai', 'ATP 500', 'Hard', '44.2%', '1529', '1996', 'Daniil Medvedev'],
                ['Halle', 'ATP 500', 'Grass', '43.3%', '1500', '1986', 'Alexander Bublik'],
                ['Hamburg', 'ATP 500', 'Clay', '27.1%', '1284', '1916', 'Alexander Zverev'],
                ['London', 'ATP 500', 'Grass', '50.7%', '1498', '1986', 'Carlos Alcaraz Garfia'],
                ['Rio de Janeiro', 'ATP 500', 'Clay', '23.0%', '1149', '1872', 'Cameron Norrie'],
                ['Rotterdam', 'ATP 500', 'Hard', '50.5%', '1597', '2018', 'Daniil Medvedev'],
                ['Tokyo', 'ATP 500', 'Hard', '46.7%', '1448', '1970', 'Ben Shelton'],
                ['Vienna', 'ATP 500', 'Hard', '56.6%', '1584', '2013', 'Jannik Sinner'],
                ['Washington', 'ATP 500', 'Hard', '31.7%', '1493', '1920', 'Daniel Evans'],
                ["'s-Hertogenbosch", 'ATP 250', 'Grass', '26.9%', '1253', '1931', 'Tallon Griekspoor'],
                ['Adelaide', 'ATP 250', 'Hard', '27.5%', '1257', '1933', 'Soon Woo Kwon'],
                ['Adelaide 1', 'ATP 250', 'Hard', '42.8%', '1578', '2011', 'Novak Djokovic'],
                ['Antwerp', 'ATP 250', 'Hard', '14.9%', '1017', '1850', 'Alexander Bublik'],
                ['Astana', 'ATP 250', 'Hard', '18.8%', '1109', '1882', 'Adrian Mannarino'],
                ['Atlanta', 'ATP 250', 'Hard', '17.6%', '1088', '1875', 'Taylor Harry Fritz'],
                ['Auckland', 'ATP 250', 'Hard', '23.8%', '1150', '1896', 'Richard Gasquet'],
                ['Banja Luka', 'ATP 250', 'Clay', '24.9%', '1231', '1924', 'Dusan Lajovic'],
                ['Bastad', 'ATP 250', 'Clay', '27.1%', '1174', '1904', 'Andrey Rublev'],
                ['Buenos Aires', 'ATP 250', 'Clay', '24.8%', '1110', '1882', 'Carlos Alcaraz Garfia'],
                ['Chengdu', 'ATP 250', 'Hard', '19.8%', '1046', '1860', 'Alexander Zverev'],
                ['Cordoba', 'ATP 250', 'Clay', '9.4%', '890', '1806', 'Sebastian Baez'],
                ['Dallas', 'ATP 250', 'Hard', '17.1%', '1064', '1866', 'Yibing Wu'],
                ['Delray Beach', 'ATP 250', 'Hard', '18.4%', '1106', '1881', 'Taylor Harry Fritz'],
                ['Doha', 'ATP 250', 'Hard', '28.9%', '1308', '1950', 'Daniil Medvedev'],
                ['Eastbourne', 'ATP 250', 'Grass', '23.0%', '1127', '1888', 'Francisco Cerundolo'],
                ['Estoril', 'ATP 250', 'Clay', '22.3%', '1019', '1851', 'Casper Ruud'],
                ['Geneva', 'ATP 250', 'Clay', '23.6%', '1164', '1901', 'Nicolas Jarry'],
                ['Gstaad', 'ATP 250', 'Clay', '11.3%', '1006', '1846', 'Pedro Cachin'],
                ['Houston', 'ATP 250', 'Clay', '11.6%', '1013', '1849', 'Frances Tiafoe'],
                ['Kitzbuhel', 'ATP 250', 'Clay', '10.4%', '981', '1838', 'Sebastian Baez'],
                ['Los Cabos', 'ATP 250', 'Hard', '21.5%', '1020', '1851', 'Stefanos Tsitsipas'],
                ['Lyon', 'ATP 250', 'Clay', '20.1%', '1154', '1897', 'Arthur Fils'],
                ['Mallorca', 'ATP 250', 'Grass', '15.8%', '1041', '1858', 'Christopher Eubanks'],
                ['Marrakech', 'ATP 250', 'Clay', '12.6%', '942', '1824', 'Roberto Carballes Baena'],
                ['Marseille', 'ATP 250', 'Hard', '19.7%', '1133', '1890', 'Hubert Hurkacz'],
                ['Metz', 'ATP 250', 'Hard', '12.8%', '998', '1843', 'Ugo Humbert'],
                ['Montpellier', 'ATP 250', 'Hard', '21.1%', '1168', '1902', 'Jannik Sinner'],
                ['Munich', 'ATP 250', 'Clay', '21.2%', '1167', '1902', 'Holger Vitus Nodskov Rune'],
                ['Newport', 'ATP 250', 'Grass', '9.3%', '855', '1794', 'Adrian Mannarino'],
                ['Pune', 'ATP 250', 'Hard', '12.1%', '971', '1834', 'Tallon Griekspoor'],
                ['Santiago', 'ATP 250', 'Clay', '13.3%', '982', '1838', 'Nicolas Jarry'],
                ['Sofia', 'ATP 250', 'Hard', '14.5%', '964', '1832', 'Adrian Mannarino'],
                ['Stockholm', 'ATP 250', 'Hard', '23.4%', '1168', '1902', 'Gael Monfils'],
                ['Stuttgart', 'ATP 250', 'Grass', '37.5%', '1358', '1967', 'Frances Tiafoe'],
                ['Umag', 'ATP 250', 'Clay', '8.5%', '995', '1843', 'Alexei Popyrin'],
                ['Winston-Salem', 'ATP 250', 'Hard', '19.1%', '1293', '1864', 'Sebastian Baez'],
                ['Zhuhai', 'ATP 250', 'Hard', '16.2%', '1021', '1852', 'Karen Khachanov'],
                ['Jeddah', 'Others', 'Hard', '5.9%', '352', '1760', 'Hamad Medjedovic']]
"""
-- Create tournaments table
CREATE TABLE tournaments (
    id INTEGER PRIMARY KEY,
    year INTEGER,
    name VARCHAR(255),
    level INTEGER,
    surface INTEGER,
    winner VARCHAR(255),
    finalist VARCHAR(255),
    no_events INTEGER,
    participation_perc FLOAT,
    strength INTEGER,
    avg_elo INTEGER
);
"""
# Establish a connection to the MySQL database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="tennis"
)


def insert_tournaments(tournaments_info):
    with connection.cursor() as cursor:
        for tournament_data in tournaments_info:
            # Extracting tournament data
            name, level, surface, participation_perc, strength, avg_elo, winner = tournament_data

            # Insert data into the tournaments table
            query_insert = "INSERT INTO tournaments (name, level, surface, participation_perc, strength, avg_elo, winner) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_insert, (name, level, surface, float(participation_perc[:-1])/100, int(strength), avg_elo, winner))
            print("Row inserted successfully!")
    # Commit changes to the database
    connection.commit()