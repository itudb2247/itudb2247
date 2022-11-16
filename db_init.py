import psycopg2 as dbapi
import psycopg2.extras


INIT = [
    """
    CREATE TABLE IF NOT EXISTS player (
        player_id SERIAL PRIMARY KEY NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS player_goalkeeping (
        goalkeeping_id  SERIAL PRIMARY KEY NOT NULL,
        diving          INT,
        handling        INT,
        kicking         INT,
        positioning     INT,
        reflexes        INT,
        player_id       INT,     
        FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS players_mentality (
        mentality_id    SERIAL PRIMARY KEY NOT NULL,
        aggression      INT,
        interceptions   INT,
        positioning     INT,
        vision          INT,
        penalties       INT,
        composure       INT,
        player_id       INT,     
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