import psycopg2 as dbapi
import pandas as pd


INIT = [

    """
    CREATE TABLE IF NOT EXISTS player (
        player_id SERIAL PRIMARY KEY NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS player_goalkeeping (
        goalkeeping_id  SERIAL PRIMARY KEY NOT NULL,
        player_id       INT, 
        diving          INT,
        handling        INT,
        kicking         INT,
        positioning     INT,
        reflexes        INT,  
        FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS player_mentality (
        mentality_id    SERIAL PRIMARY KEY NOT NULL,
        player_id       INT, 
        aggression      INT,
        interceptions   INT,
        positioning     INT,
        vision          INT,
        penalties       INT,
        composure       INT,          
        FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """
]


def create_tables():
    hostname = 'localhost'
    database = 'Fifa'
    username = 'postgres'
    pwd = 'postgres'
    port_id = 5432

    with dbapi.connect( host = hostname,
                        dbname = database,
                        user = username,
                        password = pwd,
                        port = port_id) as connection:
        cursor = connection.cursor()
        for statement in INIT:
            cursor.execute(statement)
        connection.commit()

def insert(query, row, cur):
    values = tuple(row)
    cur.execute(query, values)

def fill_tables():

    con = dbapi.connect("host='localhost' dbname='Fifa' user='postgres' password='postgres'")
    cur = con.cursor()
    #QUERIES
    query_insert_player = """INSERT INTO player VALUES('%s')"""
    query_insert_player_goalkeeping = """INSERT INTO player_goalkeeping VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
    query_insert_player_mentality = """INSERT INTO player_mentality VALUES('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s')"""

    #CSVs
    df_players = pd.read_csv("players.csv", usecols=["int_player_id"], dtype=int)
    df_player_goalkeeping = pd.read_csv("tbl_player_goalkeeping.csv", dtype=int)
    df_player_mentality = pd.read_csv("tbl_player_mentality.csv", dtype=int)

    #INSERTION
    df_players.apply(lambda x: insert(query_insert_player, x, cur), axis=1)
    df_player_goalkeeping.apply(lambda x: insert(query_insert_player_goalkeeping, x, cur), axis=1)
    df_player_mentality.apply(lambda x: insert(query_insert_player_mentality, x, cur), axis=1)
    con.commit()
    con.close()