from flask import current_app, render_template, redirect, request, url_for, flash
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
    return render_template("player_attacking.html", player_attacking_list=player_attacking_list)

# INSERT FUNCTIONS


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


def delete_player():
    if request.method == 'POST':
        player_id = request.form['player_id']

        db = current_app.config["db"]
        db.delete_player(int(player_id))
        # get name of the player for display
        #flash('"{}" was successfully deleted!'.format())
        flash('Player "{}"  was successfully deleted!'.format(player_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player.html')


def delete_player_attacking():
    if request.method == 'POST':
        db = current_app.config["db"]
        player_id = request.form['player_id']
        # print(type(player_id),player_id)
        attacking_id = db.get_attacking_id(int(player_id))
        db.delete_player_attacking(attacking_id)
        flash('Player attacking"{}"  was successfully deleted!'.format(
            attacking_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_attacking.html')


def delete_player_profile():
    if request.method == 'POST':
        profile_id = request.form['profile_id']

        db = current_app.config["db"]
        db.delete_player_profile(profile_id)
        flash('Profile #{}  was successfully deleted!'.format(profile_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_profile.html')


def delete_player_skills():
    if request.method == 'POST':
        skills_id = request.form['skills_id']

        db = current_app.config["db"]
        db.delete_player_skills(skills_id)
        flash('Skills #{}  was successfully deleted!'.format(skills_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_skills.html')


def delete_player_goalkeeping():
    if request.method == 'POST':
        goalkeeping_id = request.form['goalkeeping_id']

        db = current_app.config["db"]
        db.delete_goalkeeping(goalkeeping_id)
        flash('Goalkeeping #{}  was successfully deleted!'.format(goalkeeping_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_goalkeeping.html')


def delete_player_mentality():
    if request.method == 'POST':
        mentality_id = request.form['mentality_id']

        db = current_app.config["db"]
        db.delete_mentality(mentality_id)
        flash('Mentality #{}  was successfully deleted!'.format(mentality_id))
        return redirect(url_for('home_page'))
    return render_template('delete_player_mentality.html')


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
