import psycopg2
import pandas as pd
import db_init
from database import Database
import classes
from flask import Flask
import view

try:
    db_init.create_tables()
    db_init.fill_tables()
except:
    print("something went wrong")


# db.insert_player(Player("Nadide Bilge Doğan", "2001-7-13", 168,
#  52, 1, 2, "CF", 3, 4, 5, "https://image", 13, "Turkish"))

# db.insert_player_attacking(PlayerAttacking(18915, 1, 2, 3, 4, 5))


def create_app():
    app = Flask(__name__)

    # configuration settings
    app.config.from_object("settings")

    # URL mapping of the associated function
    app.add_url_rule("/", view_func=view.home_page)
    app.add_url_rule("/player", view_func=view.player_page)
    app.add_url_rule("/player-attacking", view_func=view.player_attacking_page)

    # create database object
    db = Database()
    # store the database object in the configuration
    app.config["db"] = db

    return app


# The main driver function
if __name__ == '__main__':
    # Run the application
    app = create_app()
    port = app.config.get("PORT", 8080)
    app.run(host="0.0.0.0", port=port)
