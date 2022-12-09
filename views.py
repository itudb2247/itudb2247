from flask import Blueprint, render_template, request, redirect, url_for, flash
import db_init
from database import *

views = Blueprint(__name__, "views")

@views.route("/")
def home(): 
    return render_template("index.html", name="blg317e")

# ADD FUNCTIONS

@views.route('/add_player/', methods=('GET', 'POST'))
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        
        db = Database()
        db.insert_player(Player(name, "2001-1-11", 160, 48, 1, 2, "CF", 3, 4, 5, "https://image", 13, "Turkish"))
        flash('Successfully inserted new player!')
        return redirect(url_for('views.home'))
    return render_template('add_player.html')

@views.route('/add_player_profile/', methods=('GET', 'POST'))
def add_player_profile():
    if request.method == 'POST':
        player_id = request.form['player_id']
        preferred_foot = request.form['preferred_foot']
        weak_foot = request.form['weak_foot']
        skill_moves = request.form['skill_moves']
        international_reputations = request.form['international_reputations']
        work_rate = request.form['work_rate']
        body_type = request.form['body_type']
        
        db = Database()
        db.insert_player_profile(player_profile(player_id,preferred_foot ,weak_foot,skill_moves,international_reputations,work_rate,body_type))
        flash('Successfully inserted new player profile!')
        return redirect(url_for('views.home'))
    return render_template('add_player_profile.html')

@views.route('/add_player_skills/', methods=('GET', 'POST'))
def add_player_skills():
    if request.method == 'POST':
        player_id = request.form['player_id']
        dribbling = request.form['dribbling']
        curve = request.form['curve']
        fk_accuracy = request.form['fk_accuracy']
        long_passing = request.form['long_passing']
        ball_control = request.form['ball_control']
        
        db = Database()
        db.insert_player_skills(player_skills(player_id,dribbling,curve,fk_accuracy,long_passing,ball_control))
        flash('Successfully inserted new player skills!')
        return redirect(url_for('views.home'))
    return render_template('add_player_skills.html')

@views.route('/add_player_goalkeeping/', methods=('GET', 'POST'))
def add_player_goalkeeping():
    if request.method == 'POST':
        player_id = request.form['player_id']
        diving = request.form['diving']
        handling = request.form['handling']
        kicking = request.form['kicking']
        positioning = request.form['positioning']
        reflexes = request.form['reflexes']
        
        db = Database()
        db.insert_goalkeeping(Goalkeeping(diving, handling, kicking, positioning, reflexes, player_id))
        flash('Successfully inserted new player goalkeeping!')
        return redirect(url_for('views.home'))
    return render_template('add_player_goalkeeping.html')

@views.route('/add_player_mentality/', methods=('GET', 'POST'))
def add_player_mentality():
    if request.method == 'POST':
        player_id = request.form['player_id']
        aggression = request.form['aggression']
        interceptions = request.form['interceptions']
        positioning = request.form['positioning']
        vision = request.form['vision']
        penalties = request.form['penalties']
        composure = request.form['composure']

        db = Database()
        db.insert_mentality(Mentality(aggression, interceptions, positioning, vision, penalties, composure, player_id))
        #flash not working
        flash('Successfully inserted new player mentality!')
        return redirect(url_for('views.home'))
    return render_template('add_player_mentality.html')

# DELETE FUNCTIONS

@views.route('/delete_player', methods=('GET', 'POST'))
def delete_player():
    if request.method == 'POST':
        player_id = request.form['player_id']

        db = Database()
        db.delete_player(player_id)
        #get name of the player for display
        #flash('"{}" was successfully deleted!'.format())
        flash('Player "{}"  was successfully deleted!'.format(player_id))
        return redirect(url_for('views.home'))
    return render_template('delete_player.html')

@views.route('/delete_profile', methods=('GET', 'POST'))
def delete_player_profile():
    if request.method == 'POST':
        profile_id = request.form['profile_id']

        db = Database()
        db.delete_player_profile(profile_id)
        flash('Profile #{}  was successfully deleted!'.format(profile_id))
        return redirect(url_for('views.home'))
    return render_template('delete_player_profile.html')

@views.route('/delete_skills', methods=('GET', 'POST'))
def delete_player_skills():
    if request.method == 'POST':
        skills_id = request.form['skills_id']

        db = Database()
        db.delete_player_skills(skills_id)
        flash('Skills #{}  was successfully deleted!'.format(skills_id))
        return redirect(url_for('views.home'))
    return render_template('delete_player_skills.html')

@views.route('/delete_goalkeeping', methods=('GET', 'POST'))
def delete_player_goalkeeping():
    if request.method == 'POST':
        goalkeeping_id = request.form['goalkeeping_id']

        db = Database()
        db.delete_goalkeeping(goalkeeping_id)
        flash('Goalkeeping #{}  was successfully deleted!'.format(goalkeeping_id))
        return redirect(url_for('views.home'))
    return render_template('delete_player_goalkeeping.html')

@views.route('/delete_mentality', methods=('GET', 'POST'))
def delete_player_mentality():
    if request.method == 'POST':
        mentality_id = request.form['mentality_id']

        db = Database()
        db.delete_mentality(mentality_id)
        flash('Mentality #{}  was successfully deleted!'.format(mentality_id))
        return redirect(url_for('views.home'))
    return render_template('delete_player_mentality.html')


@views.route('/search_player', methods=('GET', 'POST'))
def search_player():
    if request.method == 'GET':
        return render_template('search_player.html')
    else:
        player_name = request.form['player_name']

        db = Database()
        players = db.get_player(player_name)
        return render_template('search.html', players=players)

# NOT WORKING CORRECTLY
# @views.route('/update_player', methods=('GET', 'POST'))
# def update_player(player_id):
#     if request.method == 'POST':

#         date_of_birth = request.form['date_of_birth']
#         height = request.form['height']
#         weight = request.form['weight']
#         overall_rating = request.form['overall_rating']
#         potential_rating = request.form['potential_rating']
#         best_position = request.form['best_position']
#         best_overall_rating = request.form['best_overall_rating']
#         value = request.form['value']
#         wage = request.form['wage']
#         player_image_url = request.form['player_image_url']
#         team_id = request.form['team_id']
#         nationality = request.form['nationality']
#         print("xx")
#         db = Database()
#         db.update_player(date_of_birth, height, weight, overall_rating,potential_rating, best_position, best_overall_rating, value, wage,player_image_url,nationality,team_id,player_id)
#         flash('Player "{}"  was successfully updated!'.format(player_id))
#         return redirect(url_for('views.home'))
#     return render_template('update_player.html')

