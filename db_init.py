import psycopg2
import pandas as pd
INIT = [
    """
    CREATE TABLE IF NOT EXISTS team(
        team_id INTEGER NOT NULL,
        PRIMARY KEY (team_id)
    )
""",
"""
    CREATE TABLE IF NOT EXISTS player(
        player_id INTEGER NOT NULL,
        player_name VARCHAR(200) NOT NULL UNIQUE,
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
        attacking_id INTEGER NOT NULL,
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
    query_insert_player = """INSERT INTO player VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s', '%s', '%s', '%s', '%s','%s')"""
    query_insert_player_attacking = """INSERT INTO player_attacking VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
    query_insert_player_power = """INSERT INTO player_power VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
    query_insert_player_movement = """INSERT INTO player_movement VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

    #CSVs
    df_player = pd.read_csv("../csv/tbl_player.csv",usecols=["int_player_id","str_player_name","dt_date_of_birth","int_height","int_weight","int_overall_rating","int_potential_rating","str_best_position","int_best_overall_rating"	,"int_value","int_wage"	,"str_player_image_url","int_team_id","str_nationality"])
    df_player_attacking = pd.read_csv("../csv/tbl_player_attacking.csv", dtype=int)
    df_player_power = pd.read_csv("./csv/tbl_player_power.csv", dtype=int)
    df_player_movement = pd.read_csv("./csv/tbl_player_power.csv", dtype=int)

    #INSERTION
    df_player.apply(lambda x: insert(query_insert_player, x), axis=1)
    df_player_attacking.apply(lambda x: insert(query_insert_player_attacking, x), axis=1)
    df_player_power.apply(lambda x: insert(query_insert_player_power, x), axis=1)
    df_player_movement.apply(lambda x: insert(query_insert_player_movement, x), axis=1)



fill_tables()
con.commit()
con.close()

