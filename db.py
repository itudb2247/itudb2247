import psycopg2
import pandas as pd


con = psycopg2.connect("host='localhost' dbname='Fifa' user='postgres' password='postgres'")
cur = con.cursor()

arg_create_table_player = """CREATE TABLE player(
                            player_id INTEGER PRIMARY KEY
                    )"""
#cur.execute(arg_create_table_player)
#con.commit()


arg_create_table_player_power =  """CREATE TABLE player_power(
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
                    )"""
#cur.execute(arg_create_table_player_power)
#sdasddsdsf
#con.commit()

def insert_player(row):
    arg_insert_player = """INSERT INTO player VALUES('%s')"""
    values = (row[0], )
    cur.execute(arg_insert_player, values)

def insert_player_power(row):
    arg_insert_player_power = """INSERT INTO player_power VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
    values = tuple(row.values)
    cur.execute(arg_insert_player_power, values)

df_players = pd.read_csv("./csv/players.csv")
con.commit()
df_player_power = pd.read_csv("./csv/tbl_player_power.csv")
con.commit()

#numpy.in64 oludugundan sıkıntı
#integer a çevir


#df.apply(lambda x: insert_db(x["jk"], x["scrape_time"], x["zipcode"], c), axis=1)
df_players.apply(insert_player, axis=1)
df_player_power.apply(insert_player_power, axis=1)




con.commit()
con.close()