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
#db.insert_player(Player("Nadide Bilge Doğan", "2001-7-13", 168, 52, 1, 2, "CF", 3, 4, 5, "https://image", 13, "Turkish"))

#db.insert_player_attacking(PlayerAttacking( 18915,1, 2,3, 4, 5))

app=flask.Flask(__name__)
#URL mapping of the associated function
@app.route('/')

#Specify the server response to return
def first_application(): 
 return 'Welcome hÃ¼soo'
 
#The main driver function 
if __name__ == '__main__': 
 #Run the application 
 app.run()

