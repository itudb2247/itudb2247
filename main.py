import psycopg2
import pandas as pd
import db_init
from database import *
import classes
import flask

try:
    db_init.create_tables()
    db_init.fill_tables()
except:
    print("something went wrong")

db = Database()
db.insert_player(Player("Nadide Bilge Doğan", "2001-7-13", 168, 52, 1,
                        2, "CF", 3, 4, 5, "https://image", 13, "Turkish"))
# serial does not working

db.insert_player_attacking(PlayerAttacking(19003, 1, 2,
                                           3, 4, 5))

