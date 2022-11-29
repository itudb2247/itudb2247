import psycopg2
import pandas as pd
INIT = [
    """
    CREATE TABLE IF NOT EXISTS team(
        team_id SERIAL PRIMARY KEY NOT NULL
    )
""",
    """
    CREATE TABLE IF NOT EXISTS player(
        player_id SERIAL NOT NULL,
        player_name VARCHAR(200) NOT NULL,
        date_of_birth DATE,
        height INTEGER,
        weight INTEGER,
        overall_rating INTEGER,
        potential_rating INTEGER,
        best_position VARCHAR(10),
        best_overall_rating INTEGER,
        value INTEGER,
        wage INTEGER,
        player_image_url VARCHAR(200),
        team_id INTEGER NOT NULL,
        nationality VARCHAR(30),
        PRIMARY KEY (player_id),
        FOREIGN KEY (team_id)
            REFERENCES team (team_id)
            ON UPDATE CASCADE ON DELETE SET NULL
    )
""",
    """
    CREATE TABLE IF NOT EXISTS player_attacking(
        attacking_id SERIAL NOT NULL,
        player_id INTEGER NOT NULL UNIQUE,
        crossing INTEGER,
        finishing INTEGER,
        heading_accuracy INTEGER,
        short_passing INTEGER,
        volleys INTEGER,
        PRIMARY KEY (attacking_id),
        FOREIGN KEY (player_id)
            REFERENCES player (player_id)
            ON UPDATE CASCADE ON DELETE SET NULL 
    )
"""
]


def create_tables():
    hostname = 'localhost'
    database = 'Fifa'
    username = 'postgres'
    pwd = 'postgres'
    port_id = 5432
    with psycopg2.connect(host=hostname,
                          dbname=database,
                          user=username,
                          password=pwd,
                          port=port_id) as connection:
        cursor = connection.cursor()
        for statement in INIT:
            cursor.execute(statement)
        connection.commit()
        cursor.close()


def insert(query, row, cursor):
    values = tuple(row)
    cursor.execute(query, values)


def fill_tables():

    connection = psycopg2.connect(
        "host='localhost' dbname='Fifa' user='postgres' password='postgres'")
    cursor = connection.cursor()

    # QUERIES
    query_insert_team = """INSERT INTO team (team_id) VALUES(%s)"""
    query_insert_player = """INSERT INTO player VALUES(%s, %s, %s, '%s', '%s', '%s', '%s',%s,'%s', '%s', '%s', %s, '%s',%s)"""
    query_insert_player_attacking = """INSERT INTO player_attacking VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

    # CSVs
    df_team = pd.read_csv("../csv/tbl_team.csv",
                          usecols=["int_team_id"], dtype=int)
    df_player = pd.read_csv("../csv/tbl_player.csv", usecols=["int_player_id", "str_player_name", "dt_date_of_birth", "int_height", "int_weight", "int_overall_rating",
                            "int_potential_rating", "str_best_position", "int_best_overall_rating", "int_value", "int_wage", "str_player_image_url", "int_team_id", "str_nationality"])
    # convert int_team_id data type from float to int
    df_player["int_team_id"] = df_player["int_team_id"].fillna(1).astype('int64')

    # df_player = df_player.drop_duplicates(subset=["str_player_name"])
    df_player_attacking = pd.read_csv(
        "../csv/tbl_player_attacking.csv", dtype=int)
    print(df_player_attacking.iloc[-1])


    # INSERTION
    df_team.apply(lambda x: insert(query_insert_team, x, cursor), axis=1)
    df_player.apply(lambda x: insert(query_insert_player, x, cursor), axis=1)
    df_player_attacking.apply(lambda x: insert(query_insert_player_attacking, x, cursor), axis=1)

    connection.commit()
    cursor.close()
    connection.close()

