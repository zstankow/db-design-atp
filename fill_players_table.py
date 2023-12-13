import pymysql

# Establish a connection to the MySQL database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="nathszpil97",
    database="tennis"
)

NAME = 2
BEST_RANK = 1
COUNTRY = 3


def insert_player_in_table(players_info):
    with connection.cursor() as cursor:
        for player_data in players_info:
            # Check if the name already exists in the players table
            query_check = "SELECT COUNT(*) FROM players WHERE name = %s"
            cursor.execute(query_check, (player_data[2],))
            player_count = cursor.fetchone()[0]

            if player_count == 0:
                # Insert data into the players table
                query_insert = "INSERT INTO players (name, best_rank, country_id) VALUES (%s, %s, %s)"
                cursor.execute(query_insert, (player_data[NAME], int(player_data[BEST_RANK]), player_data[COUNTRY]))
                print("Row inserted successfully!")
            else:
                print("Player already exists in the table.")

    # Commit changes to the database
    connection.commit()


example_info = [['1', '1', 'Novak Djokovic', 'SRB', '-', '-'], ['2', '1', 'Roger Federer', 'SUI', '-', '-'],
                ['3', '1', 'Andy Murray', 'GBR', '-', '-'], ['4', '1', 'Rafael Nadal', 'ESP', '-', '-'],
                ['5', '3', 'David Ferrer', 'ESP', '-', '-'], ['6', '4', 'Tomas Berdych', 'CZE', '-', '-'],
                ['7', '3', 'Juan Martin Del Potro', 'ARG', '-', '-'], ['8', '5', 'Jo Wilfried Tsonga', 'FRA', '-', '-'],
                ['9', '8', 'Janko Tipsarevic', 'SRB', '-', '-'], ['10', '7', 'Richard Gasquet', 'FRA', '-', '-'],
                ['11', '9', 'Nicolas Almagro', 'ESP', '-', '-'], ['12', '10', 'Juan Monaco', 'ARG', '-', '-'],
                ['13', '3', 'Milos Raonic', 'CAN', '-', '-'], ['14', '8', 'John Isner', 'USA', '-', '-'],
                ['15', '3', 'Marin Cilic', 'CRO', '-', '-'], ['16', '6', 'Gilles Simon', 'FRA', '-', '-'],
                ['17', '3', 'Stan Wawrinka', 'SUI', '-', '-'], ['18', '13', 'Alexandr Dolgopolov', 'UKR', '-', '-'],
                ['19', '4', 'Kei Nishikori', 'JPN', '-', '-'], ['20', '16', 'Philipp Kohlschreiber', 'GER', '-', '-'],
                ['21', '2', 'Tommy Haas', 'GER', '-', '-'], ['22', '11', 'Sam Querrey', 'USA', '-', '-'],
                ['23', '18', 'Andreas Seppi', 'ITA', '-', '-'], ['24', '7', 'Fernando Verdasco', 'ESP', '-', '-'],
                ['25', '8', 'Mikhail Youzhny', 'RUS', '-', '-'], ['26', '14', 'Jerzy Janowicz', 'POL', '-', '-'],
                ['27', '7', 'Mardy Fish', 'USA', '-', '-'], ['28', '18', 'Florian Mayer', 'GER', '-', '-'],
                ['29', '8', 'Jurgen Melzer', 'AUT', '-', '-'], ['30', '24', 'Martin Klizan', 'SVK', '-', '-'],
                ['31', '8', 'Radek Stepanek', 'CZE', '-', '-'], ['32', '25', 'Jeremy Chardy', 'FRA', '-', '-'],
                ['33', '21', 'Thomaz Bellucci', 'BRA', '-', '-'], ['34', '19', 'Marcel Granollers', 'ESP', '-', '-'],
                ['35', '25', 'Julien Benneteau', 'FRA', '-', '-'], ['36', '8', 'Marcos Baghdatis', 'CYP', '-', '-'],
                ['37', '5', 'Kevin Anderson', 'RSA', '-', '-'], ['38', '12', 'Viktor Troicki', 'SRB', '-', '-'],
                ['39', '1', 'Andy Roddick', 'USA', '-', '-'], ['40', '12', 'Feliciano Lopez', 'ESP', '-', '-'],
                ['41', '13', 'Jarkko Nieminen', 'FIN', '-', '-'], ['42', '32', 'Pablo Andujar', 'ESP', '-', '-'],
                ['43', '33', 'Denis Istomin', 'UZB', '-', '-'], ['44', '3', 'Nikolay Davydenko', 'RUS', '-', '-'],
                ['45', '9', 'Fabio Fognini', 'ITA', '-', '-'], ['46', '7', 'David Goffin', 'BEL', '-', '-'],
                ['47', '18', 'Benoit Paire', 'FRA', '-', '-'], ['48', '3', 'Grigor Dimitrov', 'BUL', '-', '-'],
                ['49', '39', 'Marinko Matosevic', 'AUS', '-', '-'], ['50', '17', 'Albert Ramos', 'ESP', '-', '-'],
                ['51', '44', 'Lukas Lacko', 'SVK', '-', '-'], ['52', '17', 'Bernard Tomic', 'AUS', '-', '-'],
                ['53', '21', 'Michael Llodra', 'FRA', '-', '-'], ['54', '50', 'Alejandro Falla', 'COL', '-', '-'],
                ['55', '43', 'Grega Zemlja', 'SLO', '-', '-'], ['56', '33', 'Robin Haase', 'NED', '-', '-'],
                ['57', '28', 'Santiago Giraldo', 'COL', '-', '-'], ['58', '12', 'Paul Henri Mathieu', 'FRA', '-', '-'],
                ['59', '33', 'Yen Hsun Lu', 'TPE', '-', '-'], ['60', '47', 'Go Soeda', 'JPN', '-', '-'],
                ['61', '52', 'Brian Baker', 'USA', '-', '-'], ['62', '26', 'Victor Hanescu', 'ROU', '-', '-'],
                ['63', '19', 'Xavier Malisse', 'BEL', '-', '-'], ['64', '33', 'Paolo Lorenzi', 'ITA', '-', '-'],
                ['65', '35', 'Benjamin Becker', 'GER', '-', '-'], ['66', '37', 'Carlos Berlocq', 'ARG', '-', '-'],
                ['67', '21', 'Gilles Muller', 'LUX', '-', '-'], ['68', '52', 'Igor Sijsling', 'NED', '-', '-'],
                ['69', '40', 'Ryan Harrison', 'USA', '-', '-'], ['70', '48', 'Daniel Gimeno Traver', 'ESP', '-', '-'],
                ['71', '21', 'Leonardo Mayer', 'ARG', '-', '-'], ['72', '29', 'Ivan Dodig', 'CRO', '-', '-'],
                ['73', '26', 'Lukas Rosol', 'CZE', '-', '-'], ['74', '41', 'Lukasz Kubot', 'POL', '-', '-'],
                ['75', '59', 'Bjorn Phau', 'GER', '-', '-'], ['76', '23', 'Guillermo Garcia Lopez', 'ESP', '-', '-'],
                ['77', '6', 'Gael Monfils', 'FRA', '-', '-'], ['78', '39', 'Andrey Kuznetsov', 'RUS', '-', '-'],
                ['79', '60', 'Tatsuma Ito', 'JPN', '-', '-'], ['80', '9', 'Roberto Bautista Agut', 'ESP', '-', '-'],
                ['81', '65', 'Evgeny Donskoy', 'RUS', '-', '-'], ['82', '3', 'David Nalbandian', 'ARG', '-', '-'],
                ['83', '1', 'Lleyton Hewitt', 'AUS', '-', '-'], ['84', '36', 'Simone Bolelli', 'ITA', '-', '-'],
                ['85', '39', 'Horacio Zeballos', 'ARG', '-', '-'], ['86', '43', 'Aljaz Bedene', 'SLO', '-', '-'],
                ['87', '60', 'Michael Russell', 'USA', '-', '-'], ['88', '25', 'Filippo Volandri', 'ITA', '-', '-'],
                ['89', '71', 'Jurgen Zopp', 'EST', '-', '-'], ['90', '24', 'Olivier Rochus', 'BEL', '-', '-'],
                ['91', '50', 'Ruben Ramirez Hidalgo', 'ESP', '-', '-'],
                ['92', '81', 'Guillaume Rufin', 'FRA', '-', '-'], ['93', '38', 'Steve Darcis', 'BEL', '-', '-'],
                ['94', '68', 'Blaz Kavcic', 'SLO', '-', '-'], ['95', '70', 'Flavio Cipolla', 'ITA', '-', '-'],
                ['96', '22', 'Albert Montanes', 'ESP', '-', '-'], ['97', '20', 'Guido Pella', 'ARG', '-', '-'],
                ['98', '64', 'Tobias Kamke', 'GER', '-', '-'], ['99', '79', 'Adrian Ungur', 'ROU', '-', '-'],
                ['100', '14', 'Ivo Karlovic', 'CRO', '-', '-']]

insert_player_in_table(example_info)
