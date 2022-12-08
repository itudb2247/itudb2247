from flask import current_app, render_template
import classes

# Specify the server response to return
def home_page():
    return render_template("index.html")

def player_page():
    db = current_app.config["db"]
    players = db.get_player_list()
    return render_template("player.html")

def player_attacking_page():
    db = current_app.config["db"]
    player_attacking_list = db.get_player_attacking_list()
    return render_template("player-attacking.html",player_attacking_list = player_attacking_list)