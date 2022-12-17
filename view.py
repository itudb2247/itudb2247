from flask import current_app, render_template, redirect, request, url_for, flash
import classes
from flask_login.utils import login_required
from forms import LoginForm, SignupForm
from user import User, get_user
from passlib.hash import pbkdf2_sha256 as hasher
from flask_login import login_user, logout_user, current_user

# Specify the server response to return
def home_page():
    return render_template("index.html")

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

def signup_page():
    form = SignupForm()
    db = current_app.config["db"]
    if form.validate_on_submit():
        username = form.data["username"]
        search_user = get_user(username)
        if search_user is not None:
            flash("Username taken.")
        else:
            password = form.data["password"]
            if len(password) < 5:
                flash("Password must be longer than 5 characters.")
            else:
                hashed_password = hasher.hash(password)
                db.insert_user(username, hashed_password)
                user_ = User(username, password)
                flash("You have signed up and logged in.")
                login_user(user_)
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
    return render_template("register.html", form=form)


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
    if request.method == "POST":
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
        url = request.form["url"]
        nationality = request.form["nationality"]

        db = current_app.config["db"]
        db.insert_player(classes.Player(name, birthday, height, weight, overall_rating,
                         potential_rating, best_position, best_overall_rating, value, wage, 
                         url, team, nationality))
        flash('Successfully inserted new player!')
        return redirect(url_for("player_page"))
    return render_template("add_player.html")

@login_required
def add_player_attacking():
    if request.method == "POST":
        player_id = request.form["player_id"]
        crossing = request.form["crossing"]
        finishing = request.form["finishing"]
        heading_accuracy = request.form["heading_accuracy"]
        short_passing = request.form["short_passing"]
        volleys = request.form["volleys"]

        db = current_app.config["db"]
        db.insert_player_attacking(classes.PlayerAttacking(
            player_id, crossing, finishing, heading_accuracy, short_passing, volleys))
        flash('Successfully inserted new player attacking!')
        return redirect(url_for("player_attacking_page"))
    return render_template("add_player_attacking.html")

@login_required
def add_player_profile():
    if request.method == 'POST':
        player_id = request.form['player_id']
        preferred_foot = request.form['preferred_foot']
        weak_foot = request.form['weak_foot']
        skill_moves = request.form['skill_moves']
        international_reputations = request.form['international_reputations']
        work_rate = request.form['work_rate']
        body_type = request.form['body_type']

        db = current_app.config["db"]
        db.insert_player_profile(classes.player_profile(
            player_id, preferred_foot, weak_foot, skill_moves, international_reputations, work_rate, body_type))
        flash('Successfully inserted new player profile!')
        return redirect(url_for('home_page'))
    return render_template('add_player_profile.html')

@login_required
def add_player_skills():
    if request.method == 'POST':
        player_id = request.form['player_id']
        dribbling = request.form['dribbling']
        curve = request.form['curve']
        fk_accuracy = request.form['fk_accuracy']
        long_passing = request.form['long_passing']
        ball_control = request.form['ball_control']

        db = current_app.config["db"]
        db.insert_player_skills(classes.player_skills(
            player_id, dribbling, curve, fk_accuracy, long_passing, ball_control))
        flash('Successfully inserted new player skills!')
        return redirect(url_for('home_page'))
    return render_template('add_player_skills.html')

@login_required
def add_player_goalkeeping():
    if request.method == 'POST':
        player_id = request.form['player_id']
        diving = request.form['diving']
        handling = request.form['handling']
        kicking = request.form['kicking']
        positioning = request.form['positioning']
        reflexes = request.form['reflexes']

        db = current_app.config["db"]
        db.insert_goalkeeping(classes.Goalkeeping(
            diving, handling, kicking, positioning, reflexes, player_id))
        flash('Successfully inserted new player goalkeeping!')
        return redirect(url_for('home_page'))
    return render_template('add_player_goalkeeping.html')

@login_required
def add_player_mentality():
    if request.method == 'POST':
        player_id = request.form['player_id']
        aggression = request.form['aggression']
        interceptions = request.form['interceptions']
        positioning = request.form['positioning']
        vision = request.form['vision']
        penalties = request.form['penalties']
        composure = request.form['composure']

        db = current_app.config["db"]
        db.insert_mentality(classes.Mentality(
            aggression, interceptions, positioning, vision, penalties, composure, player_id))
        # flash not working
        flash('Successfully inserted new player mentality!')
        return redirect(url_for('home_page'))
    return render_template('add_player_mentality.html')

# DELETE FUNCTION
@login_required
def delete_player(player_id):
    db = current_app.config["db"]
    db.delete_player(int(player_id))
    # get name of the player for display
    #flash('"{}" was successfully deleted!'.format())
    flash('Player "{}"  was successfully deleted!'.format(player_id))
    return redirect(url_for('player_page'))

@login_required
def delete_player_attacking(attacking_id):
    db = current_app.config["db"]
    db.delete_player_attacking(attacking_id)
    flash('Player attacking"{}"  was successfully deleted!'.format(
            attacking_id))
    return redirect(url_for('player_attacking_page'))

@login_required
def delete_player_profile():
    if request.method == 'POST':
        profile_id = request.form['profile_id']

        db = current_app.config["db"]
        db.delete_player_profile(profile_id)
        flash('Profile #{}  was successfully deleted!'.format(profile_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_profile.html')

@login_required
def delete_player_skills():
    if request.method == 'POST':
        skills_id = request.form['skills_id']

        db = current_app.config["db"]
        db.delete_player_skills(skills_id)
        flash('Skills #{}  was successfully deleted!'.format(skills_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_skills.html')

@login_required
def delete_player_goalkeeping():
    if request.method == 'POST':
        goalkeeping_id = request.form['goalkeeping_id']

        db = current_app.config["db"]
        db.delete_goalkeeping(goalkeeping_id)
        flash('Goalkeeping #{}  was successfully deleted!'.format(goalkeeping_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_goalkeeping.html')

@login_required
def delete_player_mentality():
    if request.method == 'POST':
        mentality_id = request.form['mentality_id']

        db = current_app.config["db"]
        db.delete_mentality(mentality_id)
        flash('Mentality #{}  was successfully deleted!'.format(mentality_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_mentality.html')

# UPDATE FUNCTIONS
@login_required
def update_player(player_id):
    db = current_app.config["db"]
    player = db.get_player(player_id)
    player_list = list(player)
    if request.method == "POST":
        if(request.form["name"]!=''):
            player_list[1] = request.form["name"]
        if(request.form["date_of_birth"]!=''):
            player_list[2] = request.form["date_of_birth"]
        if(request.form["height"]!=''):
            player_list[3] = request.form["height"]
        if(request.form["weight"]!=''):
            player_list[4] = request.form["weight"]
        if(request.form["potential_rating"]!=''):
            player_list[5] = request.form["potential_rating"]
        if(request.form["overall_rating"]!=''):
            player_list[6] = request.form["overall_rating"]
        if(request.form["best_position"]!=''):
            player_list[7] = request.form["best_position"]
        if(request.form["overall_rating"]!=''):
            player_list[8] = request.form["overall_rating"]
        if(request.form["value"]!=''):
            player_list[9] = request.form["value"]
        if(request.form["wage"]!=''):
            player_list[10] = request.form["wage"]
        if(request.form["team_id"]!=''):
            player_list[11] = request.form["team_id"]
        if(request.form["url"]!=''):
            player_list[12] = request.form["url"]
        if(request.form["nationality"]!=''):
            player_list[13] = request.form["nationality"]
        
        db.update_player(classes.Player( player_name=player_list[1], date_of_birth=player_list[2], height = player_list[3], weight=player_list[4], overall_rating=player_list[5],
                 potential_rating=player_list[6], best_position=player_list[7], best_overall_rating=player_list[8], value=player_list[9], wage=player_list[10],
                 player_image_url=player_list[11], team_id=player_list[12], nationality=player_list[13], player_id=player_list[0]))
        flash('Successfully inserted new player!')
        return redirect(url_for("player_page"))
    return render_template("update_player.html")

@login_required
def update_player_attacking(attacking_id):
    db = current_app.config["db"]
    player_attacking = db.get_player_attacking(attacking_id)
    player_attacking_list = list(player_attacking)
    if request.method == "POST":
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
        flash('Successfully inserted new player attacking!')
        return redirect(url_for("player_attacking_page"))
    return render_template("update_player_attacking.html", name = player_attacking[0])

# SEARCH FUNCTIONS
"""@views.route('/search_player', methods=('GET', 'POST'))
def search_player():
    if request.method == 'GET':
        return render_template('search_player.html')
    else:
        player_name = request.form['player_name']

        db = Database()
        players = db.get_player(player_name)
        return render_template('search.html', players=players)"""
