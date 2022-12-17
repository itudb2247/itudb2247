import psycopg2
import pandas as pd
import db_init
from database import *
import classes
from views import views
import flask

# db_init.create_tables()
# db_init.fill_tables()


#db = Database()
# db.insert_player(Player("Nadide Bilge Doğan", "2001-7-13", 168, 52, 1, 2, "CF", 3, 4, 5, "https://image", 13, "Turkish"))
# db.insert_mentality(Mentality(1, 1, 1, 1, 1, 1, 18915))
# db.insert_goalkeeping(Goalkeeping(1, 1, 1, 1, 1, 18915))
#db.insert_player_skills(player_skills(18915, 1, 1, 1, 1, 1))

#db.insert_player_attacking(PlayerAttacking( 18915,1, 2,3, 4, 5))

app=flask.Flask(__name__)
#URL mapping of the associated function
app.secret_key = "abc" 
app.register_blueprint(views, url_prefix = "/")

#Specify 
 
#The main driver function 
if __name__ == '__main__': 
    #db_init.create_tables()
    #db_init.fill_tables()
    app.run(debug=True,port=8000)