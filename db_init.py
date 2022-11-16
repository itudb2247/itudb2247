import psycopg2 as dbapi

INIT = [
      """
    CREATE TABLE IF NOT EXISTS player(
        player_id SERIAL NOT NULL,
        PRIMARY KEY (player_id)
    )
""",
    """
    CREATE TABLE IF NOT EXISTS player_profile(
        profile_id SERIAL NOT NULL ,
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
        skill_id  SERIAL NOT NULL ,
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

""" 
]


def create_tables():
    hostname = 'localhost'
    database = 'Fifa'
    username = 'postgres'
    pwd = 'postgres'
    port_id = 5432
    conn = None

    with dbapi.connect( host = hostname,
                        dbname = database,
                        user = username,
                        password = pwd,
                        port = port_id) as connection:
        cursor = connection.cursor()
        for statement in INIT:
            cursor.execute(statement)
        connection.commit()
def insert_player(row,cur):
    query_insert_player = """INSERT INTO player VALUES('%s')"""
    values = tuple(row)
    cur.execute(query_insert_player, values)
def insert_player_power(row,cur):
    query_insert_player_profile = """INSERT INTO player_profile VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
    values = tuple(row)
    cur.execute(query_insert_player_profile, values)
