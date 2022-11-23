import psycopg2
import pandas as pd
INIT = [
      """
    CREATE TABLE IF NOT EXISTS player(
        player_id INTEGER NOT NULL,
        PRIMARY KEY (player_id)
    )
""",
    """
    CREATE TABLE IF NOT EXISTS player_profile(
        profile_id INTEGER NOT NULL ,
        skill_moves INTEGER,
        international_reputations INTEGER,
        work_rate VARCHAR(80),
        body_type VARCHAR(80),
        preferred_foot VARCHAR(80),
        weak_foot INTEGER,
        player_id INTEGER,
        PRIMARY KEY (profile_id),
        FOREIGN KEY (player_id)
            REFERENCES player (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
""",
    """
    CREATE TABLE IF NOT EXISTS player_skills(
        skill_id INTEGER NOT NULL ,
        dribbling INTEGER,
        curve INTEGER,
        fk_accuracy INTEGER,
        long_passing INTEGER,
        ball_control INTEGER,
        player_id INTEGER,
        PRIMARY KEY (skill_id),
        FOREIGN KEY (player_id)
            REFERENCES player (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
""",
"""CREATE TABLE IF NOT EXISTS player_power(
                            power_id INTEGER PRIMARY KEY,
                            strength INTEGER,
                            long_shots INTEGER,
                            shot_power INTEGER,
                            jumping INTEGER,
                            stamina INTEGER,
                            player_id INTEGER,
                            FOREIGN KEY (player_id) 
                                REFERENCES player (player_id)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                    )""",
"""CREATE TABLE IF NOT EXISTS player_movement(
                            movement_id INTEGER PRIMARY KEY,
                            reactions_id INTEGER,
                            balance INTEGER,
                            acceleration INTEGER,
                            sprint_speed INTEGER,
                            agility INTEGER,
                            player_id INTEGER,
                            FOREIGN KEY (player_id) 
                                REFERENCES player (player_id)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                    )"""
]
def create_tables():
    hostname = 'localhost'
    database = 'Fifa'
    username = 'postgres'
    pwd = 'postgres'
    port_id = 5432
    conn = None
    with psycopg2.connect( host = hostname,
                        dbname = database,
                        user = username,
                        password = pwd,
                        port = port_id) as connection:
        cursor = connection.cursor()
        for statement in INIT:
            cursor.execute(statement)
        connection.commit()

create_tables()
con = psycopg2.connect("host='localhost' dbname='Fifa' user='postgres' password='postgres'")
cur = con.cursor()

def insert(query, row):
    values = tuple(row)
    cur.execute(query, values)

def fill_tables():
    #QUERIES
    query_insert_player = """INSERT INTO player VALUES('%s')"""
    query_insert_player_power = """INSERT INTO player_power VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
    query_insert_player_movement = """INSERT INTO player_movement VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

    #CSVs
    df_players = pd.read_csv("./csv/players.csv", usecols=["int_player_id"], dtype=int)
    df_player_power = pd.read_csv("./csv/tbl_player_power.csv", dtype=int)
    df_player_movement = pd.read_csv("./csv/tbl_player_power.csv", dtype=int)

    #INSERTION
    df_players.apply(lambda x: insert(query_insert_player, x), axis=1)
    df_player_power.apply(lambda x: insert(query_insert_player_power, x), axis=1)
    df_player_movement.apply(lambda x: insert(query_insert_player_movement, x), axis=1)



fill_tables()
con.commit()
con.close()

