from flask import current_app, render_template, redirect, request, url_for, flash
import classes
from flask_login.utils import login_required
from forms import LoginForm, SignupForm, UploadFileForm
from user import User, get_user
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os

# Specify the server response to return
def home_page():
    db = current_app.config["db"]
    if request.method == 'GET':
        return render_template('index.html')
    else:
        option = request.form['options']
        if option == "player":
            player_name = request.form['search']
            result = db.get_player_name(player_name)
            return render_template('player_search_results.html', players=result, player_name=player_name)
        elif option == "team":
            team_name = request.form['search']
            result = db.get_team_name(team_name)      
            return render_template('team_search_results.html', teams=result, team_name=team_name)

def view_player_results(player_name):
    db = current_app.config["db"]
    if request.method == "GET":
        result = db.get_player_name(player_name)
        return render_template('player_search_results.html',players=result, player_name=player_name)
    else: 
        form_player_ids = request.form.getlist("player_id")
        for player_id in form_player_ids:
            db.delete_player(int(player_id))
        return redirect(url_for("view_player_results", player_name=player_name))

def view_team_results(team_name):
    db = current_app.config["db"]
    if request.method == "GET":
        result = db.get_team_name(team_name)
        return render_template('team_search_results.html',teams=result, team_name=team_name)
    else: 
        form_team_ids = request.form.getlist("team_id")
        for team_id in form_team_ids:
            db.delete_team(int(team_id))
        return redirect(url_for("view_team_results", team_name=team_name))


def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))


# file upload
def user_profile():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),current_app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        filename = secure_filename(file.filename)
        return render_template('user_profile.html', form=form,filename=filename)
    return render_template('user_profile.html', form=form)

def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='files/' + filename), code=301)

def player_page():
    db = current_app.config["db"]
    players = db.get_player_list()
    return render_template("player.html", player_list=players)


def player_attacking_page():
    db = current_app.config["db"]
    player_attacking_list = db.get_player_attacking_list()
    # print(player_attacking_list)
    return render_template("player_attacking.html", player_attacking_list=player_attacking_list)

# INSERT FUNCTIONS

@login_required
def add_player():
    db = current_app.config["db"]
    if request.method == "POST":
        valid = validate_player_form(request.form)
        if not valid:
            return render_template("add_player.html", values=request.form, teams = db.view_teams(),)

        name = request.form["name"]
        birthday = request.form["date_of_birth"]
        height = request.form["height"]
        weight = request.form["weight"]
        potential_rating = request.form["potential_rating"]
        overall_rating = request.form["overall_rating"]
        best_position = request.form["best_position"]
        best_overall_rating = request.form["best_overall_rating"]
        value = request.form["value"]
        wage = request.form["wage"]
        team = request.form["team_id"]
        if request.form["url"] =='':
            url = "https://upload.wikimedia.org/wikipedia/commons/b/bc/Unknown_person.jpg"
        else:
            url = request.form["url"]
        nationality = request.form["nationality"]

        db.insert_player(classes.Player(name, birthday, height, weight, overall_rating,
                         potential_rating, best_position, best_overall_rating, value, wage,
                         url, team, nationality))
        player_id = db.get_player_id_by_name_birthday(name,birthday)
        
        return redirect(url_for('player_full_profile',player_id=player_id[0]))
    return render_template("add_player.html", values=request.form, teams = db.view_teams(),)


@login_required
def add_player_attacking():
    player_id=request.args.get("player_id")
    if request.method == "POST":
        valid = validate_player_attacking(request.form)
        if not valid:
            return render_template("add_player_attacking.html", values=request.form,)

        # player_id = request.form["player_id"]
        crossing = request.form["crossing"]
        finishing = request.form["finishing"]
        heading_accuracy = request.form["heading_accuracy"]
        short_passing = request.form["short_passing"]
        volleys = request.form["volleys"]

        db = current_app.config["db"]
        db.insert_player_attacking(classes.PlayerAttacking(
            player_id, crossing, finishing, heading_accuracy, short_passing, volleys))
        return redirect(url_for('player_full_profile',player_id=player_id))
    return render_template("add_player_attacking.html", values=request.form,)


@login_required
def add_player_profile():
    player_id=request.args.get("player_id")
    if request.method == 'POST':
        preferred_foot = request.form['preferred_foot']
        weak_foot = request.form['weak_foot']
        skill_moves = request.form['skill_moves']
        international_reputations = request.form['international_reputations']
        work_rate = request.form['work_rate']
        body_type = request.form['body_type']

        db = current_app.config["db"]
        db.insert_player_profile(classes.player_profile(
            player_id, preferred_foot, weak_foot, skill_moves, international_reputations, work_rate, body_type))
        return redirect(url_for('player_full_profile',player_id=player_id))
    return render_template('add_player_profile.html')

@login_required
def add_player_skills():
    player_id=request.args.get("player_id")
    if request.method == 'POST':
        valid = validate_player_skills_form(request.form)
        if not valid:
            return render_template("add_player_skills.html", values=request.form,)
        dribbling = request.form['dribbling']
        curve = request.form['curve']
        fk_accuracy = request.form['fk_accuracy']
        long_passing = request.form['long_passing']
        ball_control = request.form['ball_control']

        db = current_app.config["db"]
        db.insert_player_skills(classes.player_skills(
            player_id, dribbling, curve, fk_accuracy, long_passing, ball_control))
        return redirect(url_for('player_full_profile',player_id=player_id))
    return render_template('add_player_skills.html', values = request.form,)

@login_required
def add_player_goalkeeping():
    player_id=request.args.get("player_id")
    if request.method == 'POST':
        valid = validate_player_goalkeeping_form(request.form)
        if not valid:
            return render_template("add_player_goalkeeping.html", values=request.form,)
        diving = request.form['diving']
        handling = request.form['handling']
        kicking = request.form['kicking']
        positioning = request.form['positioning']
        reflexes = request.form['reflexes']

        db = current_app.config["db"]
        db.insert_goalkeeping(classes.Goalkeeping(
            diving, handling, kicking, positioning, reflexes, player_id))
        return redirect(url_for('player_full_profile',player_id=player_id))
    return render_template('add_player_goalkeeping.html', values=request.form)

@login_required
def add_player_mentality():
    player_id=request.args.get("player_id")
    if request.method == 'POST':
        valid = validate_player_mentality_form(request.form)
        if not valid:
            return render_template("add_player_mentality.html", values = request.form,)
        aggression = request.form['aggression']
        interceptions = request.form['interceptions']
        positioning = request.form['positioning']
        vision = request.form['vision']
        penalties = request.form['penalties']
        composure = request.form['composure']

        db = current_app.config["db"]
        db.insert_mentality(classes.Mentality(
            aggression, interceptions, positioning, vision, penalties, composure, player_id))
        return redirect(url_for('player_full_profile',player_id=player_id))
    return render_template('add_player_mentality.html',values=request.form)

@login_required
def add_team():
    db = current_app.config["db"]
    if request.method == "POST":
        team_name=request.form['team_name']
        unique_name = True
        if (db.get_team_by_name(team_name)is not None):
            unique_name = False
        valid = validate_team_form(request.form,unique_name)
        if not valid:
            return render_template("team/add_team.html", values=request.form,)
        league=request.form['league']
        overall=request.form['overall']
        attack=request.form['attack']
        midfield=request.form['midfield']
        defense=request.form['defense']
        international_prestige=request.form['international_prestige']
        domestic_prestige=request.form['domestic_prestige']
        transfer_budget=request.form['transfer_budget']

        db = current_app.config["db"]
        db.insert_team(classes.Team(team_name,league,overall,attack,midfield,defense,international_prestige,
        domestic_prestige,transfer_budget))
        team_id=db.get_player_team_id(team_name)
        return redirect(url_for('view_tactics',team_id=team_id))
    return render_template('team/add_team.html', values=request.form,)

@login_required
def add_team_tactics():
    team_id=request.args.get("team_id")
    if request.method =='POST':
        defensive_style=request.form['defensive_style']
        team_width=request.form['team_width']
        depth=request.form['depth']
        offensive_style=request.form['offensive_style']
        width=request.form['width']
        players_in_box=request.form['players_in_box']
        corners=request.form['corners']
        freekicks=request.form['freekicks']
        db = current_app.config["db"]
        db.insert_team_tactics(classes.Team_tactics(defensive_style,team_width,depth,offensive_style,width,players_in_box,
        corners,freekicks,team_id))
        return redirect(url_for('view_tactics',team_id=team_id))
    return render_template('team_tactics/add_team_tactics.html')

# DELETE FUNCTION
@login_required
def delete_player(player_id):
    team_id=request.args.get("team_id")
    db = current_app.config["db"]
    db.delete_player(int(player_id))
    return redirect(url_for('view_players_of_team', team_id=team_id))

@login_required
def delete_player_attacking(attacking_id,player_id):

    db = current_app.config["db"]
    db.delete_player_attacking(attacking_id)
    return redirect(url_for('player_full_profile',player_id=player_id))

@login_required
def delete_player_profile(profile_id,player_id):
    db = current_app.config["db"]
    db.delete_player_profile(profile_id)
    return redirect(url_for('player_full_profile',player_id=player_id))

@login_required
def delete_player_skills(skills_id,player_id):
    db = current_app.config["db"]
    db.delete_player_skills(skills_id)
    return redirect(url_for('player_full_profile',player_id=player_id))

@login_required
def delete_player_goalkeeping(goalkeeping_id,player_id):
    db = current_app.config["db"]
    db.delete_goalkeeping(goalkeeping_id)
    flash('Goalkeeping #{}  was successfully deleted!'.format(goalkeeping_id))
    return redirect(url_for('player_full_profile',player_id=player_id))

@login_required
def delete_player_mentality(mentality_id,player_id):
    db = current_app.config["db"]
    db.delete_mentality(mentality_id)
    return redirect(url_for('player_full_profile',player_id=player_id))

@login_required
def delete_player_power(power_id,player_id):
    db = current_app.config["db"]
    db.delete_power(power_id)
    return redirect(url_for('player_full_profile',player_id=player_id))

@login_required
def delete_player_movement(movement_id,player_id):
    db = current_app.config["db"]
    db.delete_movement(movement_id)
    return redirect(url_for('player_full_profile',player_id=player_id))


@login_required
def delete_team(team_id):
    league=request.args.get("league")
    db = current_app.config["db"]
    db.delete_team(int(team_id))
    return redirect(url_for('view_teams_of_league', league=league))


@login_required
def delete_team_tactics(tactic_id,team_id):

    db = current_app.config["db"]
    db.delete_team_tactics(tactic_id)
    return redirect(url_for('view_tactics',team_id=team_id))

# UPDATE FUNCTIONS
@login_required
def update_player(player_id):
    db = current_app.config["db"]
    player = db.get_player(player_id)
    player_list = list(player)
    if request.method == "POST":
        valid = validate_player_form(request.form)
        if not valid:
            return render_template("update_player.html", values=request.form,)

        if(request.form["name"] != ''):
            player_list[1] = request.form["name"]
        if(request.form["date_of_birth"]!=''):
            player_list[2] = request.form["date_of_birth"]
        if(request.form["height"]!=''):
            player_list[3] = request.form["height"]
        if(request.form["weight"]!=''):
            player_list[4] = request.form["weight"]
        if(request.form["overall_rating"]!=''):
            player_list[5] = request.form["overall_rating"]
        if(request.form["potential_rating"]!=''):
            player_list[6] = request.form["potential_rating"]
        if(request.form["best_position"]!=''):
            player_list[7] = request.form["best_position"]
        if(request.form["best_overall_rating"]!=''):
            player_list[8] = request.form["best_overall_rating"]
        if(request.form["value"]!=''):
            player_list[9] = request.form["value"]
        if(request.form["wage"]!=''):
            player_list[10] = request.form["wage"]
        if(request.form["url"]!=''):
            player_list[11] = request.form["url"]
        if(request.form["team_id"]!=''):
            player_list[12] = request.form["team_id"]
        if(request.form["nationality"]!=''):
            player_list[13] = request.form["nationality"]
        
        db.update_player(classes.Player(player_name=player_list[1], date_of_birth=player_list[2], height=player_list[3], weight=player_list[4], overall_rating=player_list[5],
                 potential_rating=player_list[6], best_position=player_list[
                     7], best_overall_rating=player_list[8], value=player_list[9], wage=player_list[10],
                 player_image_url=player_list[11], team_id=player_list[12], nationality=player_list[13], player_id=player_list[0]))

        team_id = db.get_team_id(player_list[0])
        team_id = team_id[0]
        team = db.get_team_by_id(team_id)
        return redirect(url_for('view_players_of_team', team_id=team[0], team_name=team[1]))
    return render_template("update_player.html", values=request.form,)

@login_required
def update_team():
    db = current_app.config["db"]
    if request.method=='POST':
        team_id=request.args.get("team_id")
        print(team_id)
        team = list(db.get_team_by_id(team_id))
        valid = validate_team_form(request.form,True)
        if not valid:
            return render_template("team/update_team.html", values=request.form,)
        if (request.form['league'] != ''):
            team[2]=request.form['league']
        if (request.form['overall'] != ''):
            team[3]=request.form['overall']
        if (request.form['attack'] != ''):
            team[4]=request.form['attack']
        if (request.form['midfield'] != ''):
            team[5]=request.form['midfield']
        if (request.form['defense'] != ''):
            team[6]=request.form['defense']
        if (request.form['international_prestige'] != ''):
            team[7]=request.form['international_prestige']
        if (request.form['domestic_prestige'] != ''):
            team[8]=request.form['domestic_prestige']
        if (request.form['transfer_budget'] != ''):
            team[9]=request.form['transfer_budget']
        db.update_team(team[2],team[3],team[4],team[5],team[6],team[7],team[8],team[9],team_id)
        return redirect(url_for('view_team'))
    return render_template("team/update_team.html", values=request.form,)

@login_required
def update_team_tactics(tactic_id):
    db = current_app.config["db"]
    tactic = db.get_team_tactics(tactic_id)
    print(tactic_id)
    tactic_list = list(tactic)
    if request.method == "POST":
        if(request.form["defensive_style"]!=''):
            tactic_list[2] = request.form["defensive_style"]
        if(request.form["team_width"]!=''):
            tactic_list[3] = request.form["team_width"]
        if(request.form["depth"]!=''):
            tactic_list[4] = request.form["depth"]
        if(request.form["offensive_style"]!=''):
            tactic_list[5] = request.form["offensive_style"]
        if(request.form["width"]!=''):
            tactic_list[6] = request.form["width"]
        if(request.form["players_in_box"]!=''):
            tactic_list[7] = request.form["players_in_box"]
        if(request.form["corners"]!=''):
            tactic_list[8] = request.form["corners"]
        if(request.form["freekicks"]!=''):
            tactic_list[9] = request.form["freekicks"]
        new_tactic = classes.Team_tactics( tactic_id=tactic_list[0], team_id=tactic_list[1], defensive_style = tactic_list[2], 
                                            team_width = tactic_list[3], depth = tactic_list[4], 
                                            offensive_style = tactic_list[5], width = tactic_list[6], 
                                            players_in_box = tactic_list[7],corners = tactic_list[8]
                                            ,freekicks = tactic_list[9])
        db.update_team_tactics(new_tactic)
        return redirect(url_for('view_tactics',team_id=tactic_list[1]))
    return render_template("team/update_tactics.html")

@login_required
def update_player_attacking(attacking_id):
    db = current_app.config["db"]
    player_attacking = db.get_player_attacking(attacking_id)
    player_attacking_list = list(player_attacking)
    if request.method == "POST":
        valid = validate_player_attacking(request.form)
        if not valid:
            return render_template("update_player_attacking.html",name = player_attacking[0], values=request.form,)

        if(request.form["crossing"]!=''):
            player_attacking_list[3] = request.form["crossing"]
        if(request.form["finishing"]!=''):
            player_attacking_list[4] = request.form["finishing"]
        if(request.form["heading_accuracy"]!=''):
            player_attacking_list[5] = request.form["heading_accuracy"]
        if(request.form["short_passing"]!=''):
            player_attacking_list[6] = request.form["short_passing"]
        if(request.form["volleys"]!=''):
            player_attacking_list[7] = request.form["volleys"]

        new_attacking = classes.PlayerAttacking(attacking_id=player_attacking_list[1], player_id = player_attacking_list[2], 
                                           crossing = player_attacking_list[3], finishing = player_attacking_list[4], 
                                           heading_accuracy = player_attacking_list[5], short_passing = player_attacking_list[6], 
                                           volleys = player_attacking_list[7])
        db.update_player_attacking(new_attacking)
        return redirect(url_for('player_full_profile',player_id=player_attacking_list[2]))
    return render_template("update_player_attacking.html", name = player_attacking[0], values=request.form,)

@login_required
def update_player_mentality(mentality_id):
    valid = validate_player_mentality_form(request.form)
    if not valid:
        return render_template("update_player_mentality.html", values=request.form,)
    db = current_app.config["db"]
    mentality = db.get_player_mentality(mentality_id)
    mentality_list = list(mentality)
    if request.method == "POST":
        if(request.form["aggression"]!=''):
            mentality_list[2] = request.form["aggression"]
        if(request.form["interceptions"]!=''):
            mentality_list[3] = request.form["interceptions"]
        if(request.form["positioning"]!=''):
            mentality_list[4] = request.form["positioning"]
        if(request.form["vision"]!=''):
            mentality_list[5] = request.form["vision"]
        if(request.form["penalties"]!=''):
            mentality_list[6] = request.form["penalties"]
        if(request.form["composure"]!=''):
            mentality_list[7] = request.form["composure"]
        
        db.update_mentality(classes.Mentality(mentality_id=mentality_list[0], player_id=mentality_list[1], aggression=mentality_list[2], interceptions=mentality_list[3], positioning=mentality_list[4], vision=mentality_list[5], penalties=mentality_list[6], composure=mentality_list[7]))
        return redirect(url_for('player_full_profile',player_id=mentality_list[1]))
    return render_template("update_player_mentality.html", values=request.form)

@login_required
def update_player_goalkeeping(goalkeeping_id):
    valid = validate_player_goalkeeping_form(request.form)
    if not valid:
        return render_template("update_player_goalkeeping.html", values=request.form,)
    db = current_app.config["db"]
    db = current_app.config["db"]
    goalkeeping = db.get_player_goalkeeping(goalkeeping_id)
    goalkeeping_list = list(goalkeeping)
    if request.method == "POST":
        if(request.form["diving"]!=''):
            goalkeeping_list[2] = request.form["diving"]
        if(request.form["handling"]!=''):
            goalkeeping_list[3] = request.form["handling"]
        if(request.form["kicking"]!=''):
            goalkeeping_list[4] = request.form["kicking"]
        if(request.form["positioning"]!=''):
            goalkeeping_list[5] = request.form["positioning"]
        if(request.form["reflexes"]!=''):
            goalkeeping_list[6] = request.form["reflexes"]
        
        db.update_goalkeeping(classes.Goalkeeping(goalkeeping_id=goalkeeping_list[0],player_id=goalkeeping_list[1], diving=goalkeeping_list[2], handling=goalkeeping_list[3], kicking=goalkeeping_list[4], positioning=goalkeeping_list[5], reflexes=goalkeeping_list[6]))
        return redirect(url_for('player_full_profile',player_id=goalkeeping_list[1]))
    return render_template("update_player_goalkeeping.html", values=request.form)

@login_required
def update_player_profile(profile_id):
    db = current_app.config["db"]
    player_profile = db.get_player_profile(profile_id)
    player_profile_list = list(player_profile)
    if request.method == "POST":
        if(request.form["preferred_foot"]!=''):
            player_profile_list[2] = request.form["preferred_foot"]
        if(request.form["weak_foot"]!=''):
            player_profile_list[3] = request.form["weak_foot"]
        if(request.form["skill_moves"]!=''):
            player_profile_list[4] = request.form["skill_moves"]
        if(request.form["international_reputations"]!=''):
            player_profile_list[5] = request.form["international_reputations"]
        if(request.form["work_rate"]!=''):
            player_profile_list[6] = request.form["work_rate"]
        if(request.form["body_type"]!=''):
            player_profile_list[7] = request.form["body_type"]
        db.update_player_profile(classes.player_profile(profile_id=player_profile_list[0], player_id=player_profile_list[1], preferred_foot=player_profile_list[2], weak_foot=player_profile_list[3], skill_moves = player_profile_list[4], international_reputations=player_profile_list[5], work_rate=player_profile_list[6],
                 body_type=player_profile_list[7]))
        return redirect(url_for('player_full_profile',player_id=player_profile_list[1]))
    return render_template("update_player_profile.html")

@login_required
def update_player_skills(skill_id):
    valid = validate_player_skills_form(request.form)
    if not valid:
        return render_template("update_player_skills.html", values=request.form,)
    db = current_app.config["db"]
    player = db.get_player_skills(skill_id)
    player_list = list(player)
    if request.method == "POST":
        if(request.form["dribbling"]!=''):
            player_list[2] = request.form["dribbling"]
        if(request.form["curve"]!=''):
            player_list[3] = request.form["curve"]
        if(request.form["fk_accuracy"]!=''):
            player_list[4] = request.form["fk_accuracy"]
        if(request.form["long_passing"]!=''):
            player_list[5] = request.form["long_passing"]
        if(request.form["ball_control"]!=''):
            player_list[6] = request.form["ball_control"]
        db.update_player_skills(classes.player_skills( dribbling=player_list[2], curve=player_list[3], fk_accuracy = player_list[4], long_passing=player_list[5], ball_control=player_list[6],
                  skill_id=player_list[0],player_id=player_list[1]))
        return redirect(url_for('player_full_profile',player_id=player_list[1]))
    return render_template("update_player_skills.html",values=request.form)


# MAHMUT

@login_required
def add_player_power():
    player_id=request.args.get("player_id")
    if request.method == 'POST':
        valid = validate_player_power_form(request.form)
        if not valid:
            return render_template("power/add_player_power.html", values=request.form,)
        strength = request.form['strength']
        long_shots = request.form['long_shots']
        shot_power = request.form['shot_power']
        jumping = request.form['jumping']
        stamina = request.form['stamina']

        db = current_app.config["db"]
        db.insert_power(classes.Power(
            player_id, strength, long_shots, shot_power, jumping, stamina))
        return redirect(url_for('player_full_profile',player_id=player_id))
    return render_template('power/add_player_power.html', values = request.form,)



@login_required
def add_player_movement():
    player_id=request.args.get("player_id")
    if request.method == 'POST':
        valid = validate_player_movement_form(request.form)
        if not valid:
            return render_template("movement/add_player_movement.html", values=request.form,)
        reactions = request.form['reactions']
        balance = request.form['balance']
        acceleration = request.form['acceleration']
        sprint_speed = request.form['sprint_speed']
        agility = request.form['agility']

        db = current_app.config["db"]
        db.insert_movement(classes.Movement(
            player_id, reactions, balance, acceleration, sprint_speed, agility))
        return redirect(url_for('player_full_profile',player_id=player_id))
    return render_template('movement/add_player_movement.html', values = request.form,)


@login_required
def update_player_power(power_id):
    valid = validate_player_power_form(request.form)
    if not valid:
        return render_template("power/update_player_power.html", values=request.form,)
    db = current_app.config["db"]
    power = db.get_power(power_id)
    # power_id, player_id, strength, long_shots, shot_power, jumping, stamina
    power_list = list(power)
    if request.method == "POST":
        print(power_list[5])
        if(request.form["strength"]!=''):
            power_list[2] = request.form["strength"]
        if(request.form["long_shots"]!=''):
            power_list[3] = request.form["long_shots"]
        if(request.form["shot_power"]!=''):
            power_list[4] = request.form["shot_power"]
        if(request.form["jumping"]!=''):
            power_list[5] = request.form["jumping"]
        if(request.form["stamina"]!=''):
            power_list[6] = request.form["stamina"]        
            #Power(player_id, strength, long_shots, shot_power, jumping, stamina, power_id)
        db.update_power(classes.Power(power_list[1], power_list[2], power_list[3], power_list[4], power_list[5], power_list[6], power_list[0]))
        return redirect(url_for('player_full_profile',player_id=power_list[1]))
    return render_template("power/update_player_power.html", values=request.form, )

@login_required
def update_player_movement(movement_id):
    valid = validate_player_movement_form(request.form)
    if not valid:
        return render_template("movement/update_player_movement.html", values=request.form,)
    db = current_app.config["db"]
    movement = db.get_movement(movement_id)
    # movement_id, player_id , reactions, balance, acceleration, sprint_speed, agility 
    movement_list = list(movement)
    if request.method == "POST":
        print(movement_list[0])
        if(request.form["reactions"]!=''):
            movement_list[2] = request.form["reactions"]
        if(request.form["balance"]!=''):
            movement_list[3] = request.form["balance"]
        if(request.form["acceleration"]!=''):
            movement_list[4] = request.form["acceleration"]
        if(request.form["sprint_speed"]!=''):
            movement_list[5] = request.form["sprint_speed"]
        if(request.form["agility"]!=''):
            movement_list[6] = request.form["agility"]
        # movement_id, player_id , reactions, balance, acceleration, sprint_speed, agility 
        db.update_movement(classes.Movement(movement_list[1], movement_list[2], movement_list[3], movement_list[4], movement_list[5], movement_list[6], movement_list[0]))
        return redirect(url_for('player_full_profile',player_id=movement_list[1]))
    return render_template("movement/update_player_movement.html", values=request.form,)

def validate_player_power_form(form):
    form.data = {}
    form.errors = {}

    strength = form.get("strength")
    if not strength:
        form.data["strength"] = None
    else:
        strength = int(strength)
        if (strength < 0) or (strength > 100):
            form.errors["strength"] = "strength not in valid range."
        else:
            form.data["strength"] = strength

    long_shots  = form.get("long_shots")
    if not long_shots :
        form.data["long_shots"] = None
    else:
        long_shots  = int(long_shots )
        if (long_shots  < 0) or (long_shots  > 100):
            form.errors["long_shots"] = "long_shots not in valid range."
        else:
            form.data["long_shots"] = long_shots 

    shot_power = form.get("shot_power")
    if not shot_power:
        form.data["shot_power"] = None

    else:
        shot_power = int(shot_power)
        if (shot_power < 0) or (shot_power> 100):
            form.errors["shot_power"] = "shot_power not in valid range."
        else:
            form.data["shot_power"] = shot_power

    jumping = form.get("jumping")
    if not jumping:
        form.data["jumping"] = None

    else:
        jumping = int(jumping)
        if (jumping < 0) or (jumping > 100):
            form.errors["jumping"] = "jumping not in valid range."
        else:
            form.data["jumping"] = jumping

    stamina= form.get("stamina")
    if not stamina:
        form.data["stamina"] = None

    else:
        stamina = int(stamina)
        if (stamina < 0) or (stamina > 100):
            form.errors["stamina"] = "stamina not in valid range."
        else:
            form.data["stamina"] = stamina

    return len(form.errors) == 0



def validate_player_movement_form(form):
    form.data = {}
    form.errors = {}

    reactions = form.get("reactions")
    if not reactions:
        form.data["reactions"] = None
    else:
        reactions = int(reactions)
        if (reactions < 0) or (reactions > 100):
            form.errors["reactions"] = "reactions not in valid range."
        else:
            form.data["reactions"] = reactions

    balance  = form.get("balance")
    if not balance :
        form.data["balance"] = None
    else:
        balance  = int(balance )
        if (balance  < 0) or (balance  > 100):
            form.errors["balance"] = "balance not in valid range."
        else:
            form.data["balance"] = balance 

    acceleration = form.get("acceleration")
    if not acceleration:
        form.data["acceleration"] = None

    else:
        acceleration = int(acceleration)
        if (acceleration < 0) or (acceleration> 100):
            form.errors["acceleration"] = "acceleration not in valid range."
        else:
            form.data["acceleration"] = acceleration

    sprint_speed = form.get("sprint_speed")
    if not sprint_speed:
        form.data["sprint_speed"] = None

    else:
        sprint_speed = int(sprint_speed)
        if (sprint_speed < 0) or (sprint_speed > 100):
            form.errors["sprint_speed"] = "sprint_speed not in valid range."
        else:
            form.data["sprint_speed"] = sprint_speed

    agility= form.get("agility")
    if not agility:
        form.data["agility"] = None

    else:
        agility = int(agility)
        if (agility < 0) or (agility > 100):
            form.errors["agility"] = "agility not in valid range."
        else:
            form.data["agility"] = agility

    return len(form.errors) == 0

## DARIA

def navbar():
    return render_template('navbar.html')

def view_team():
    db = current_app.config["db"]
    if request.method == "GET":
        teams=db.view_teams()
        return render_template('team/teams.html',teams=teams)
    else:
        form_team_ids = request.form.getlist("team_id")
        for team_id in form_team_ids:
            db.delete_team(int(team_id))
        return redirect(url_for("view_team"))

def view_player():
    # db = current_app.config["db"]
    # players=db.view_players()
    # return render_template('team/players.html',players=players)

    db = current_app.config["db"]
    if request.method == "GET":
        players=db.view_players()
        return render_template('team/players.html',players=players)
    else: 
        form_player_ids = request.form.getlist("player_id")
        for player_id in form_player_ids:
            db.delete_player(int(player_id))
        return redirect(url_for("view_player"))



def view_all_tactics():
    db = current_app.config["db"]
    tactics=db.view_all_tactics()
    return render_template('team_tactics/tactics.html',tactics=tactics)

def view_league():
    db = current_app.config["db"]
    leagues=db.view_leagues()
    return render_template('team/leagues.html',leagues=leagues)

def view_teams_of_league():
    if request.method=='GET':
        league=request.args.get("league")
        db = current_app.config["db"]
        teams=db.view_teams_of_league(league)
    return render_template('team/teams_cards.html',teams=teams)

def view_players_of_team():
    team_id=request.args.get("team_id")
    db = current_app.config["db"]
    
    players=db.view_players_of_team(team_id)
    return render_template('team/view_players_of_team.html',players=players)

def view_tactics():
    team_id=request.args.get("team_id")
    db = current_app.config["db"]
    tactic=db.view_tactics(team_id)
    return render_template('team_tactics/team_based_tactics.html',tactic=tactic, team_id=team_id)

def player_full_profile():
    player_id=request.args.get("player_id")
    db = current_app.config["db"]
    attacking=db.get_attacking_p(player_id)
    player_profile=db.get_player_profile_p(player_id)
    player_skills=db.get_player_skills_p(player_id)
    player_goalkeeping=db.get_player_goalkeeping_p(player_id)
    player_mentality=db.get_player_mentality_p(player_id)
    player_power=db.get_player_power_p(player_id)
    player_movement=db.get_player_movement_p(player_id)
    return render_template('player_full_profile.html',player_id=player_id,attacking=attacking,
    player_profile=player_profile,player_skills=player_skills,
    player_goalkeeping=player_goalkeeping,player_mentality=player_mentality,
    player_power=player_power,player_movement=player_movement)

def validate_player_skills_form(form):
    form.data = {}
    form.errors = {}

    dribbling = form.get("dribbling")
    if not dribbling:
        form.data["dribbling"] = None
    else:
        dribbling = int(dribbling)
        if (dribbling < 0) or (dribbling > 100):
            form.errors["dribbling"] = "Dribbling not in valid range."
        else:
            form.data["dribbling"] = dribbling

    curve  = form.get("curve")
    if not curve :
        form.data["curve"] = None
    else:
        curve  = int(curve )
        if (curve  < 0) or (curve  > 100):
            form.errors["curve"] = "Curve not in valid range."
        else:
            form.data["curve"] = curve 

    fk_accuracy = form.get("fk_accuracy")
    if not fk_accuracy:
        form.data["fk_accuracy"] = None

    else:
        fk_accuracy = int(fk_accuracy)
        if (fk_accuracy < 0) or (fk_accuracy> 100):
            form.errors["fk_accuracy"] = "Fk Accuracy not in valid range."
        else:
            form.data["fk_accuracy"] = fk_accuracy

    long_passing = form.get("long_passing")
    if not long_passing:
        form.data["long_passing"] = None

    else:
        long_passing = int(long_passing)
        if (long_passing < 0) or (long_passing > 100):
            form.errors["long_passing"] = "Long Passing not in valid range."
        else:
            form.data["long_passing"] = long_passing

    ball_control= form.get("ball_control")
    if not ball_control:
        form.data["ball_control"] = None

    else:
        ball_control = int(ball_control)
        if (ball_control < 0) or (ball_control > 100):
            form.errors["ball_control"] = "Ball Control not in valid range."
        else:
            form.data["ball_control"] = ball_control

    return len(form.errors) == 0

def validate_player_form(form):
    form.data = {}
    form.errors = {}
    
    height = form.get("height")
    if not height:
        form.data["height"] = None
    else:
        height = int(height)
        if (height < 20) or (height > 1000):
            form.errors["height"] = "Height not in valid range."
        else:
            form.data["height"] = height

    weight = form.get("weight")
    if not weight:
        form.data["weight"] = None
    else:
        weight = int(weight)
        if (weight < 20) or (weight > 1000):
            form.errors["weight"] = "Weight not in valid range."
        else:
            form.data["weight"] = weight
    
    potential_rating = form.get("potential_rating")
    if not potential_rating:
        form.data["potential_rating"] = None

    else:
        potential_rating = int(potential_rating)
        if (potential_rating < 0):
            form.errors["potential_rating"] = "Potential rating not in valid range."
        else:
            form.data["potential_rating"] = potential_rating
    
    best_overall_rating = form.get("best_overall_rating")
    if not best_overall_rating:
        form.data["best_overall_rating"] = None

    else:
        best_overall_rating = int(best_overall_rating)
        if (best_overall_rating < 0):
            form.errors["best_overall_rating"] = "Best overall rating not in valid range."
        else:
            form.data["best_overall_rating"] = best_overall_rating
    
    value = form.get("value")
    if not value:
        form.data["value"] = None

    else:
        value = int(value)
        if (value < 0):
            form.errors["value"] = "Value not in valid range."
        else:
            form.data["value"] = value
    
    wage = form.get("wage")
    if not wage:
        form.data["wage"] = None

    else:
        wage = int(wage)
        if (wage < 0):
            form.errors["wage"] = "Wage not in valid range."
        else:
            form.data["wage"] = wage

    return len(form.errors) == 0
    
def validate_player_attacking(form):
    form.data = {}
    form.errors = {}

    crossing = form.get("crossing")
    if not crossing:
        form.data["crossing"] = None
    else:
        crossing = int(crossing)
        if (crossing < 0):
            form.errors["crossing"] = "Crossing not in valid range."
        else:
            form.data["crossing"] = crossing
    
    finishing = form.get("finishing")
    if not finishing:
        form.data["finishing"] = None
    else:
        finishing = int(finishing)
        if (finishing < 0):
            form.errors["finishing"] = "Finishing not in valid range."
        else:
            form.data["finishing"] = finishing
    
    heading_accuracy = form.get("heading_accuracy")
    if not heading_accuracy:
        form.data["heading_accuracy"] = None
    else:
        heading_accuracy = int(heading_accuracy)
        if (heading_accuracy < 0):
            form.errors["heading_accuracy"] = "Heading accuracy not in valid range."
        else:
            form.data["heading_accuracy"] = heading_accuracy
    
    short_passing = form.get("short_passing")
    if not short_passing:
        form.data["short_passing"] = None

    else:
        short_passing = int(short_passing)
        if (short_passing < 0):
            form.errors["short_passing"] = "Short passing not in valid range."
        else:
            form.data["short_passing"] = short_passing

    volleys = form.get("volleys")
    if not volleys:
        form.data["volleys"] = None
    else:
        volleys = int(volleys)
        if (volleys < 0):
            form.errors["volleys"] = "Volleys not in valid range."
        else:
            form.data["volleys"] = volleys

    return len(form.errors) == 0

def validate_player_mentality_form(form):
    form.data = {}
    form.errors = {}
    
    aggression = form.get("aggression")
    if not aggression:
        form.data["aggression"] = None
    else:
        aggression = int(aggression)
        if (aggression < 0) or (aggression > 100):
            form.errors["aggression"] = "Aggression not in valid range."
        else:
            form.data["aggression"] = aggression

    interceptions = form.get("interceptions")
    if not interceptions:
        form.data["interceptions"] = None
    else:
        interceptions = int(interceptions)
        if (interceptions < 0) or (interceptions > 100):
            form.errors["interceptions"] = "Interceptions not in valid range."
        else:
            form.data["interceptions"] = interceptions
    
    positioning = form.get("positioning")
    if not positioning:
        form.data["positioning"] = None

    else:
        positioning = int(positioning)
        if (positioning < 0) or (positioning > 100):
            form.errors["positioning"] = "Positioning not in valid range."
        else:
            form.data["positioning"] = positioning
    
    vision = form.get("vision")
    if not vision:
        form.data["vision"] = None

    else:
        vision = int(vision)
        if (vision < 0) or (vision > 100):
            form.errors["vision"] = "Vision not in valid range."
        else:
            form.data["vision"] = vision
    
    penalties = form.get("penalties")
    if not penalties:
        form.data["penalties"] = None

    else:
        penalties = int(penalties)
        if (penalties < 0) or (penalties > 100):
            form.errors["penalties"] = "Penalties not in valid range."
        else:
            form.data["penalties"] = penalties
    
    composure = form.get("composure")
    if not composure:
        form.data["composure"] = None

    else:
        composure = int(composure)
        if (composure < 0) or (composure > 100):
            form.errors["composure"] = "Composure not in valid range."
        else:
            form.data["composure"] = composure

    return len(form.errors) == 0

def validate_player_goalkeeping_form(form):
    form.data = {}
    form.errors = {}
    
    diving = form.get("diving")
    if not diving:
        form.data["diving"] = None
    else:
        diving = int(diving)
        if (diving < 0) or (diving > 100):
            form.errors["diving"] = "Diving not in valid range."
        else:
            form.data["diving"] = diving

    handling = form.get("handling")
    if not handling:
        form.data["handling"] = None
    else:
        handling = int(handling)
        if (handling < 0) or (handling > 100):
            form.errors["handling"] = "Handling not in valid range."
        else:
            form.data["handling"] = handling
    
    kicking = form.get("kicking")
    if not kicking:
        form.data["kicking"] = None

    else:
        kicking = int(kicking)
        if (kicking < 0) or (kicking > 100):
            form.errors["kicking"] = "Kicking not in valid range."
        else:
            form.data["kicking"] = kicking
    
    positioning = form.get("positioning")
    if not positioning:
        form.data["positioning"] = None

    else:
        positioning = int(positioning)
        if (positioning < 0) or (positioning > 100):
            form.errors["positioning"] = "Positioning not in valid range."
        else:
            form.data["positioning"] = positioning
    
    reflexes = form.get("reflexes")
    if not reflexes:
        form.data["reflexes"] = None

    else:
        reflexes = int(reflexes)
        if (reflexes < 0) or (reflexes > 100):
            form.errors["reflexes"] = "Reflexes not in valid range."
        else:
            form.data["reflexes"] = reflexes

    return len(form.errors) == 0

#### new validations for team ####
def validate_team_form(form,unique_name):
    form.data = {}
    form.errors = {}
    
    if unique_name == False:
        form.errors["team_name"] = "Team already exist!"
    overall = form.get("overall")
    if not overall:
        form.data["overall"] = None
    else:
        overall = int(overall)
        if (overall < 0) or (overall > 100):
            form.errors["overall"] = "Overall not in valid range."
        else:
            form.data["overall"] = overall

    attack = form.get("attack")
    if not attack:
        form.data["attack"] = None
    else:
        attack = int(attack)
        if (attack < 0) or (attack > 100):
            form.errors["attack"] = "Attack not in valid range."
        else:
            form.data["attack"] = attack
    
    midfield = form.get("midfield")
    if not midfield:
        form.data["midfield"] = None

    else:
        midfield = int(midfield)
        if (midfield < 0)or(midfield > 100):
            form.errors["midfield"] = "Midfield not in valid range."
        else:
            form.data["midfield"] = midfield
    
    defense = form.get("defense")
    if not defense:
        form.data["defense"] = None

    else:
        defense = int(defense)
        if (defense < 0) or (defense > 100):
            form.errors["defense"] = "Defense not in valid range."
        else:
            form.data["defense"] = defense
        
    domestic_prestige = form.get("domestic_prestige")
    if not domestic_prestige:
        form.data["domestic_prestige"] = None

    else:
        domestic_prestige = int(domestic_prestige)
        if (domestic_prestige < 0) or(domestic_prestige>10):
            form.errors["domestic_prestige"] = "domestic_prestige not in valid range (0-10)."
        else:
            form.data["domestic_prestige"] = domestic_prestige

    international_prestige = form.get("international_prestige")
    if not international_prestige:
        form.data["international_prestige"] = None

    else:
        international_prestige = int(international_prestige)
        if (international_prestige < 0) or (international_prestige > 10):
            form.errors["international_prestige"] = "International Prestige not in valid range (0-10)."
        else:
            form.data["international_prestige"] = international_prestige

    transfer_budget = form.get("transfer_budget")
    if not transfer_budget:
        form.data["transfer_budget"] = None

    else:
        transfer_budget = int(transfer_budget)
        if (transfer_budget < 0) :
            form.errors["transfer_budget"] = "Transfer budget not in valid range."
        else:
            form.data["transfer_budget"] = transfer_budget

    return len(form.errors) == 0