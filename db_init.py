import psycopg2 as dbapi
import pandas as pd


INIT = [

    """
      CREATE TABLE IF NOT EXISTS team(
         team_id SERIAL NOT NULL,
         team_name VARCHAR(200) NOT NULL UNIQUE,
         league VARCHAR(200),
         overall INTEGER,
         attack INTEGER,
         midfield INTEGER,
         defense INTEGER,
         international_prestige INTEGER,
         domestic_prestige INTEGER,
         transfer_budget INTEGER,
         PRIMARY KEY (team_id)
      )
     """,


    """
    CREATE TABLE IF NOT EXISTS player(
        player_id SERIAL NOT NULL,
        player_name VARCHAR(200) NOT NULL,
        date_of_birth VARCHAR(200),
        height INTEGER,
        weight INTEGER,
        overall_rating INTEGER,
        potential_rating INTEGER,
        best_position VARCHAR(10),
        best_overall_rating INTEGER,
        value INTEGER,
        wage INTEGER,
        player_image_url VARCHAR(200),
        team_id SERIAL NOT NULL,
        nationality VARCHAR(30),
        PRIMARY KEY (player_id),
        FOREIGN KEY (team_id)
            REFERENCES team (team_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS player_attacking(
        attacking_id SERIAL NOT NULL,
        player_id SERIAL NOT NULL UNIQUE,
        crossing INTEGER,
        finishing INTEGER,
        heading_accuracy INTEGER,
        short_passing INTEGER,
        volleys INTEGER,
        PRIMARY KEY (attacking_id),
        FOREIGN KEY (player_id)
            REFERENCES player (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE 
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS player_profile(
        profile_id SERIAL NOT NULL ,
        player_id SERIAL,
        preferred_foot VARCHAR(80),
        weak_foot INTEGER,
        skill_moves INTEGER,
        international_reputations INTEGER,
        work_rate VARCHAR(80),
        body_type VARCHAR(80),
        PRIMARY KEY (profile_id),
        FOREIGN KEY (player_id)
            REFERENCES player (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )

    """,
    
    """
    CREATE TABLE IF NOT EXISTS player_skills(
        skill_id  SERIAL NOT NULL ,
        player_id SERIAL,
        dribbling INTEGER,
        curve INTEGER,
        fk_accuracy INTEGER,
        long_passing INTEGER,
        ball_control INTEGER,
        PRIMARY KEY (skill_id),
        FOREIGN KEY (player_id)
            REFERENCES player (player_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """CREATE TABLE IF NOT EXISTS player_power(
                            power_id  SERIAL NOT NULL,
                            player_id SERIAL,
                            strength INTEGER,
                            long_shots INTEGER,
                            shot_power INTEGER,
                            jumping INTEGER,
                            stamina INTEGER,
                            PRIMARY KEY (power_id),
                            FOREIGN KEY (player_id) 
                                REFERENCES player (player_id)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
    )""",

    """CREATE TABLE IF NOT EXISTS player_movement(
                            movement_id  SERIAL NOT NULL,
                            player_id SERIAL,
                            reactions INTEGER,
                            balance INTEGER,
                            acceleration INTEGER,
                            sprint_speed INTEGER,
                            agility INTEGER,
                            PRIMARY KEY (movement_id),
                            FOREIGN KEY (player_id) 
                                REFERENCES player (player_id)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
    )""",

    """
    CREATE TABLE IF NOT EXISTS player_goalkeeping (
        goalkeeping_id  SERIAL NOT NULL,
        player_id       SERIAL, 
        diving          INT,
        handling        INT,
        kicking         INT,
        positioning     INT,
        reflexes        INT, 
        PRIMARY KEY (goalkeeping_id), 
        FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS player_mentality (
        mentality_id    SERIAL NOT NULL,
        player_id       SERIAL, 
        aggression      INT,
        interceptions   INT,
        positioning     INT,
        vision          INT,
        penalties       INT,
        composure       INT,  
        PRIMARY KEY (mentality_id),       
        FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,

    """
      CREATE TABLE IF NOT EXISTS team_tactics(
         tactic_id SERIAL NOT NULL,
         team_id SERIAL,
         defensive_style VARCHAR(200),
         team_width INTEGER,
         depth INTEGER,
         offensive_style VARCHAR(200),
         width INTEGER,
         players_in_box INTEGER,
         corners INTEGER,
         freekicks INTEGER,
         PRIMARY KEY (tactic_id),
         FOREIGN KEY (team_id)
            REFERENCES team (team_id)
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
    query_insert_team= """INSERT INTO team(team_name,league,overall,attack,midfield,defense,international_prestige,domestic_prestige,transfer_budget) VALUES( %s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    query_insert_player = """INSERT INTO player(player_name, date_of_birth, height, weight, overall_rating,potential_rating, best_position, best_overall_rating, value, wage,player_image_url,team_id, nationality ) VALUES( %s, %s, %s, %s, %s, %s,%s,%s, %s, %s, %s, %s,%s)"""
    query_insert_player_attacking = """INSERT INTO player_attacking(crossing, finishing,heading_accuracy, short_passing, volleys) VALUES(%s, %s, %s, %s, %s)"""
    query_insert_player_profile = """INSERT INTO player_profile(preferred_foot,weak_foot,skill_moves,international_reputations,work_rate,body_type) VALUES(  %s, '%s', '%s','%s', %s,%s)"""
    query_insert_player_skills = """INSERT INTO player_skills(dribbling,curve,fk_accuracy,long_passing,ball_control) VALUES(  '%s', '%s', '%s', '%s', '%s')"""
    query_insert_player_power = """INSERT INTO player_power(shot_power, jumping, stamina,strength,long_shots) VALUES(  '%s', '%s', '%s', '%s', '%s')"""
    query_insert_player_movement = """INSERT INTO player_movement(acceleration,sprint_speed,agility,reactions,balance) VALUES(  '%s', '%s', '%s', '%s', '%s')"""
    query_insert_player_goalkeeping = """INSERT INTO player_goalkeeping(diving,handling,kicking,positioning,reflexes) VALUES( '%s', '%s', '%s', '%s', '%s')"""
    query_insert_player_mentality = """INSERT INTO player_mentality(aggression,interceptions,positioning,vision,penalties,composure) VALUES( '%s','%s', '%s', '%s', '%s', '%s')"""
    query_insert_team_tactics= """INSERT INTO team_tactics(defensive_style,team_width,depth,offensive_style,width,players_in_box,corners,freekicks) VALUES(%s,'%s','%s',%s,'%s','%s','%s','%s')"""

    # CSVs
    df_player_profile = pd.read_csv("./data/tbl_player_profile.csv", usecols=["str_preferred_foot", "int_weak_foot", "int_skill_moves", "int_international_reputations", "str_work_rate", "str_body_type"])
    df_player_skills = pd.read_csv("./data/tbl_player_skill.csv", dtype=int, usecols=["int_dribbling", "int_curve", "int_fk_accuracy", "int_long_passing", "int_ball_control"])
    df_player_movement = pd.read_csv("./data/tbl_player_movement.csv", dtype=int, usecols=["int_acceleration", "int_sprint_speed", "int_agility", "int_reactions", "int_balance"])
    df_player_power = pd.read_csv("./data/tbl_player_power.csv", dtype=int, usecols=["int_shot_power", "int_jumping", "int_stamina", "int_strength", "int_long_shots"])
    df_player_goalkeeping = pd.read_csv("./data/tbl_player_goalkeeping.csv", dtype=int, usecols=["int_diving", "int_handling", "int_kicking", "int_positioning", "int_reflexes"])
    df_player_mentality = pd.read_csv("./data//tbl_player_mentality.csv", dtype=int, usecols=["int_aggression", "int_interceptions", "int_positioning", "int_vision", "int_penalties", "int_composure"])
    df_team= pd.read_csv("./data/tbl_team.csv",usecols=["str_team_name","str_league","int_overall","int_attack","int_midfield","int_defence","int_international_prestige","int_domestic_prestige","int_transfer_budget"])
    df_team_tactics=pd.read_csv("./data/tbl_team_tactics.csv", usecols=["str_defensive_style","int_team_width","int_depth","str_offensive_style","int_width","int_players_in_box","int_corners","int_freekicks"])
    # fill the null team id values with -1 which is no team
    df_player = pd.read_csv("./data/tbl_player.csv", usecols=["str_player_name", "dt_date_of_birth", "int_height", "int_weight", "int_overall_rating", "int_potential_rating",
                            "str_best_position", "int_best_overall_rating", "int_value", "int_wage", "str_player_image_url", "int_team_id", "str_nationality"],dtype={"dt_date_of_birth":str})
    # fill the null team id values with -1 which is no team
    df_player["int_team_id"] = df_player["int_team_id"].fillna(682)
    df_player_attacking = pd.read_csv("./data/tbl_player_attacking.csv", dtype=int, usecols=["int_crossing", "int_finishing", "int_heading_accuracy", "int_short_passing", "int_volleys"])

    # INSERTION
    df_team.apply(lambda x: insert(query_insert_team, x, cur), axis=1)
    df_player.apply(lambda x: insert(query_insert_player, x, cur), axis=1)
    # con.commit()

    df_player_attacking.apply(lambda x: insert(
        query_insert_player_attacking, x, cur), axis=1)
    df_player_profile.apply(lambda x: insert(
        query_insert_player_profile, x, cur), axis=1)
    df_player_movement.apply(lambda x: insert(
        query_insert_player_movement, x, cur), axis=1)
    df_player_power.apply(lambda x: insert(
        query_insert_player_power, x, cur), axis=1)
    df_player_skills.apply(lambda x: insert(
        query_insert_player_skills, x, cur), axis=1)
    df_player_goalkeeping.apply(lambda x: insert(
        query_insert_player_goalkeeping, x, cur), axis=1)
    df_player_mentality.apply(lambda x: insert(
        query_insert_player_mentality, x, cur), axis=1)
    df_team_tactics.apply(lambda x:insert(
        query_insert_team_tactics, x, cur), axis=1)
    con.commit()
    con.close()