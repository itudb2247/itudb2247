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
    print("")

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
    app.add_url_rule("/", view_func=view.home_page,methods=["GET", "POST"])
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
    app.add_url_rule("/delete_player_attacking/<attacking_id>/<player_id>",view_func=view.delete_player_attacking, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_mentality/<mentality_id>/<player_id>",view_func=view.delete_player_mentality, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_goalkeeping/<goalkeeping_id>/<player_id>",view_func=view.delete_player_goalkeeping, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_skills/<skills_id>/<player_id>",view_func=view.delete_player_skills, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_profile/<profile_id>/<player_id>",view_func=view.delete_player_profile, methods=["GET", "POST"])
    
    # Update pages
    app.add_url_rule("/update_player_attacking/<attacking_id>",view_func=view.update_player_attacking, methods=["GET", "POST"])
    app.add_url_rule("/update_player/<player_id>",view_func=view.update_player, methods=["GET", "POST"])
    app.add_url_rule("/add_team",view_func=view.add_team, methods=["GET", "POST"])
    app.add_url_rule("/add_team_tactics",view_func=view.add_team_tactics, methods=["GET", "POST"])
    app.add_url_rule("/delete_team/<team_id>",view_func=view.delete_team, methods=["GET", "POST"])
    app.add_url_rule("/delete_team_tactics/<tactic_id>/<team_id>",view_func=view.delete_team_tactics, methods=["GET", "POST"])
    app.add_url_rule("/update_team",view_func=view.update_team, methods=["GET", "POST"])
    app.add_url_rule("/update_team_tactics/<tactic_id>",view_func=view.update_team_tactics, methods=["GET", "POST"])
    app.add_url_rule("/update_player_mentality/<mentality_id>",view_func=view.update_player_mentality, methods=["GET", "POST"])
    app.add_url_rule("/update_player_goalkeeping/<goalkeeping_id>",view_func=view.update_player_goalkeeping, methods=["GET", "POST"])
    app.add_url_rule("/update_player_profile/<profile_id>",view_func=view.update_player_profile, methods=["GET", "POST"])
    app.add_url_rule("/update_player_skills/<skill_id>",view_func=view.update_player_skills, methods=["GET", "POST"])



    app.add_url_rule("/view_player_results/<player_name>",view_func=view.view_player_results, methods=["GET", "POST"])
    app.add_url_rule("/view_team_results/<team_name>",view_func=view.view_team_results, methods=["GET", "POST"])

    # Mahmut
    app.add_url_rule("/add_player_power",view_func=view.add_player_power, methods=["GET", "POST"])
    app.add_url_rule("/add_player_movement",view_func=view.add_player_movement, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_movement/<movement_id>/<player_id>",view_func=view.delete_player_movement, methods=["GET", "POST"])
    app.add_url_rule("/delete_player_power/<power_id>/<player_id>",view_func=view.delete_player_power, methods=["GET", "POST"])
    app.add_url_rule("/update_player_power/<power_id>",view_func=view.update_player_power, methods=["GET", "POST"])
    app.add_url_rule("/update_player_movement/<movement_id>",view_func=view.update_player_movement, methods=["GET", "POST"])


    #DARIA
    app.add_url_rule("/navbar",view_func=view.navbar)
    app.add_url_rule("/view_team",view_func=view.view_team, methods=["GET", "POST"])
    app.add_url_rule("/view_player",view_func=view.view_player, methods=["GET", "POST"])
    app.add_url_rule("/view_all_tactics",view_func=view.view_all_tactics, methods=["GET", "POST"])
    app.add_url_rule("/view_league",view_func=view.view_league, methods=["GET", "POST"])
    app.add_url_rule("/view_teams_of_league",view_func=view.view_teams_of_league, methods=["GET", "POST"])
    app.add_url_rule("/view_players_of_team",view_func=view.view_players_of_team, methods=["GET", "POST"])
    app.add_url_rule("/view_tactics",view_func=view.view_tactics, methods=["GET", "POST"])
    app.add_url_rule("/player_full_profile",view_func=view.player_full_profile, methods=["GET", "POST"])

    #file upload
    app.add_url_rule("/user_profile",view_func=view.user_profile, methods=["GET", "POST"])
    app.add_url_rule("/display/<filename>",view_func=view.display_image, methods=["GET", "POST"])
    

    # login manager
    lm.init_app(app)
    lm.login_view = "login_page"

    # create database object
    db = Database()
    # store the database object in the configuration
    app.config["db"] = db
    app.config['UPLOAD_FOLDER'] = 'static/files'

    return app


# The main driver function
if __name__ == '__main__':
    # Run the application
    app = create_app()
    port = app.config.get("PORT", 8080)
    app.run(host="0.0.0.0", port=port)
