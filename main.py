import db_init
from database import Database
from flask import Flask
import view
from flask_login import LoginManager
from user import get_user


try:
    db_init.create_tables()
    db_init.fill_tables()
except:
    print("something went wrong")

# create login manager obj
lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.secret_key = "abc"
    # configuration settings
    app.config.from_object("settings")

    # Login - Logout
    app.add_url_rule("/login", view_func=view.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=view.logout_page)
    # app.add_url_rule("/signup", view_func=view.signup_page,methods=["GET", "POST"])

    # URL mapping of the associated function
    app.add_url_rule("/", view_func=view.home_page)
    app.add_url_rule("/player", view_func=view.player_page)
    app.add_url_rule("/player_attacking", view_func=view.player_attacking_page)
    # Insertion pages
    app.add_url_rule("/add_player", view_func=view.add_player,methods=["GET", "POST"])
    app.add_url_rule("/add_player_attacking", view_func=view.add_player_attacking, methods=["GET", "POST"])
    app.add_url_rule("/add_player_mentality",view_func=view.add_player_mentality, methods=["GET", "POST"])
    app.add_url_rule("/add_player_goalkeeping", view_func=view.add_player_goalkeeping, methods=["GET", "POST"])
    app.add_url_rule("/add_player_skills", view_func=view.add_player_skills, methods=["GET", "POST"])
    app.add_url_rule("/add_player_profile",view_func=view.add_player_profile, methods=["GET", "POST"])
    # Deletion pages
    app.add_url_rule("/delete_player/<player_id>", view_func=view.delete_player, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_attacking/<attacking_id>",view_func=view.delete_player_attacking, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_mentality",view_func=view.delete_player_mentality, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_goalkeeping",view_func=view.delete_player_goalkeeping, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_skills",view_func=view.delete_player_skills, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_profile",view_func=view.delete_player_profile, methods=["GET", "POST"])
    # Update pages
    app.add_url_rule("/update_player_attacking/<attacking_id>",view_func=view.update_player_attacking, methods=["GET", "POST"])
    app.add_url_rule("/update_player/<player_id>",view_func=view.update_player, methods=["GET", "POST"])


    # login manager
    lm.init_app(app)
    lm.login_view = "login_page"

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
