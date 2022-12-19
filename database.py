import psycopg2 as dbapi
from classes import *


class Database:
    def __init__(self):
        #check if database exists
        self.host = 'localhost'
        self.db_name = 'Fifa'
        self.user = 'postgres'
        self.password = 'postgres'
        self.port = 5432
        self.connection = dbapi.connect(host =self.host, database = self.db_name, user=self.user, password=self.password, port=self.port)
        self.cursor = self.connection.cursor()
# -------------BİLGE----------------------------------
    # player_image_url?
    def insert_player(self, player):
        statement = """INSERT INTO player(player_name,date_of_birth,height,weight,overall_rating,potential_rating,best_position,best_overall_rating,value,wage,player_image_url,team_id,nationality) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(statement, (player.player_name, player.date_of_birth, player.height, player.weight, player.overall_rating, player.potential_rating,
                                        player.best_position, player.best_overall_rating, player.value, player.wage, player.player_image_url, player.team_id, player.nationality))
        self.connection.commit()

    # can player_name be updated or not?
    def update_player(self, player):
        statement = """UPDATE player SET player_name=%s, date_of_birth=%s, height=%s, weight=%s, overall_rating=%s, potential_rating=%s, best_position=%s, best_overall_rating=%s, value=%s, wage=%s, player_image_url=%s, team_id=%s, nationality=%s WHERE (player_id = %s)"""
        self.cursor.execute(statement, (player.player_name, player.date_of_birth, player.height, player.weight, player.overall_rating, player.potential_rating,
                                        player.best_position, player.best_overall_rating, player.value, player.wage, player.player_image_url, player.team_id, player.nationality, player.player_id))
        self.connection.commit()

    def delete_player(self, player_id):
        statement = """DELETE FROM player WHERE (player_id=%s)"""
        self.cursor.execute(statement, (player_id,))
        self.connection.commit()

    def insert_player_attacking(self, player_attacking):
        statement = """INSERT INTO player_attacking(player_id,crossing,finishing,heading_accuracy,short_passing,volleys) VALUES(%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(statement, (player_attacking.player_id, player_attacking.crossing, player_attacking.finishing,
                                        player_attacking.heading_accuracy, player_attacking.short_passing, player_attacking.volleys))
        self.connection.commit()

    # can player_id be updated or not?
    def update_player_attacking(self, player_attacking):
        statement = """UPDATE player_attacking SET crossing=%s, finishing=%s, heading_accuracy=%s, short_passing=%s, volleys=%s WHERE (attacking_id = %s)"""
        self.cursor.execute(statement, (player_attacking.crossing, player_attacking.finishing,
                                        player_attacking.heading_accuracy, player_attacking.short_passing, player_attacking.volleys, player_attacking.attacking_id))
        self.connection.commit()

    def delete_player_attacking(self, player_attacking_id):
        statement = """DELETE FROM player_attacking WHERE attacking_id=%s"""
        self.cursor.execute(statement, (player_attacking_id,))
        self.connection.commit()

    def get_player(self, player_id):
        statement = """SELECT * FROM player WHERE (player_id=%s)"""
        self.cursor.execute(statement, (player_id,))
        player = self.cursor.fetchone()
        return player

    # def get_attacking_id(self, player_id):
    #     statement = """SELECT (attacking_id)FROM player_attacking WHERE (player_id=%s)"""
    #     self.cursor.execute(statement, (player_id,))
    #     attacking_id = self.cursor.fetchone()
    #     # print(attacking_id)
    #     return attacking_id

    def get_player_attacking(self, attacking_id):
        statement = """SELECT player.player_name, player_attacking.attacking_id, player_attacking.player_id, player_attacking.crossing, player_attacking.finishing, player_attacking.heading_accuracy, player_attacking.short_passing, player_attacking.volleys FROM player_attacking , player WHERE(player.player_id = player_attacking.player_id) AND (player_attacking.attacking_id = %s)"""
        self.cursor.execute(statement, (attacking_id,))
        player_attacking = self.cursor.fetchone()
        return player_attacking

    def get_player_list(self):
        self.cursor.execute(
            """SELECT * FROM player ORDER BY player_id DESC LIMIT 10""")
        return self.cursor.fetchall()

    def get_player_attacking_list(self):
        self.cursor.execute("""SELECT player.player_name, player_attacking.attacking_id, player_attacking.player_id, player_attacking.crossing, player_attacking.finishing, player_attacking.heading_accuracy, player_attacking.short_passing, player_attacking.volleys FROM player_attacking , player WHERE(player.player_id = player_attacking.player_id) """)
        return self.cursor.fetchall()

    def get_team_id(self, player_id):
        query = """SELECT team_id FROM player WHERE(player_id = %s)"""
        self.cursor.execute(query, (player_id,))
        return self.cursor.fetchone()

    def get_team_by_id(self, team_id):
        statement = """SELECT * FROM team WHERE team_id=%s"""
        self.cursor.execute(statement, (team_id,))
        team = self.cursor.fetchone()
        return team

    def get_team_by_name(self, team_name):
        statement = """SELECT * FROM team WHERE team_name=%s"""
        self.cursor.execute(statement, (team_name,))
        team = self.cursor.fetchone()
        return team

    def get_player_id_by_name_birthday(self, name, birthday):
        query = """SELECT player_id FROM  player WHERE  (player_name = %s AND date_of_birth=%s)"""
        self.cursor.execute(query, (name, birthday))
        return self.cursor.fetchone()
# -------------ANIL----------------------------------

    def insert_player_profile(self, player_profile):
        self.cursor.execute("INSERT INTO player_profile(player_id,preferred_foot ,weak_foot,skill_moves,international_reputations,work_rate,body_type) VALUES(%s, %s, %s, %s, %s,%s, %s)",
                            (player_profile.player_id ,player_profile.preferred_foot,player_profile.weak_foot,player_profile.skill_moves, player_profile.international_reputations, player_profile.work_rate, player_profile.body_type))
        self.connection.commit()

    def delete_player_profile(self, profile_id):
        self.cursor.execute(
            "DELETE FROM player_profile WHERE profile_id=%s", (profile_id,))
        self.connection.commit()

    def update_player_profile(self, player_profile):
        print(player_profile.preferred_foot)
        statement = """UPDATE player_profile SET preferred_foot=%s, weak_foot=%s, skill_moves=%s, international_reputations=%s, work_rate=%s ,body_type=%s WHERE (profile_id = %s)"""
        self.cursor.execute(statement, (player_profile.preferred_foot, player_profile.weak_foot,
                                        player_profile.skill_moves, player_profile.international_reputations, player_profile.work_rate,player_profile.body_type, player_profile.profile_id))
        self.connection.commit()

    def get_player_profile(self, profile_id):
        statement = """SELECT * FROM player_profile WHERE (profile_id=%s)"""
        self.cursor.execute(statement, (profile_id,))
        player_profile = self.cursor.fetchone()
        return player_profile

    def insert_player_skills(self, player_skills):
        self.cursor.execute("INSERT INTO player_skills(player_id,dribbling,curve,fk_accuracy,long_passing,ball_control)VALUES(%s, %s, %s, %s, %s, %s)",
                            (player_skills.player_id, player_skills.dribbling, player_skills.curve, player_skills.fk_accuracy, player_skills.long_passing, player_skills.ball_control))
        self.connection.commit()

    def delete_player_skills(self, skill_id):
        self.cursor.execute(
            "DELETE FROM player_skills WHERE skill_id=%s", (skill_id,))
        self.connection.commit()

    def get_player_skills(self, skill_id):
        statement = """SELECT * FROM player_skills WHERE (skill_id=%s)"""
        self.cursor.execute(statement, (skill_id,))
        player_skills = self.cursor.fetchone()
        return player_skills

    def update_player_skills(self, player_skills):
        statement = """UPDATE player_skills SET dribbling=%s, curve=%s, fk_accuracy=%s, long_passing=%s ,ball_control=%s WHERE (skill_id = %s)"""
        self.cursor.execute(statement, (player_skills.dribbling, player_skills.curve,
                                        player_skills.fk_accuracy, player_skills.long_passing, player_skills.ball_control, player_skills.skill_id))
        self.connection.commit()

    def get_player_team_id(self, team):
        print(team)
        print(type(team))
        query = """SELECT team_id FROM  team WHERE (team_name= %s )"""
        self.cursor.execute(query,(team,))
        return self.cursor.fetchone()

# -------------MAHMUT----------------------------------
    # player_power
    def insert_power(self, power : Power):
        self.cursor.execute(
            "INSERT INTO player_power(strength,long_shots,shot_power,jumping,stamina,player_id) VALUES({}, {}, {}, {}, {}, {})".format(*power.get_power()))
        self.connection.commit()

    def update_power(self, power : Power):
        self.cursor.execute(
            "UPDATE player_power SET strength={}, long_shots={}, shot_power={}, jumping={}, stamina={}, player_id={} WHERE (power_id={})".format(*power.get_power("update")))
        self.connection.commit()

    def delete_power(self, power_id):
        self.cursor.execute(
            "DELETE FROM player_power WHERE power_id={}".format(power_id))
        self.connection.commit()

    def get_power(self, power_id):
        self.cursor.execute(
            "SELECT * FROM player_power WHERE power_id={}".format(power_id))
        results = self.cursor.fetchone()
        return results

    # player_movement
    def insert_movement(self, movement: Movement):
        self.cursor.execute(
            "INSERT INTO player_movement(reactions,balance,acceleration,sprint_speed,agility,player_id) VALUES({}, {}, {}, {}, {}, {})".format(*movement.get_movement()))
        self.connection.commit()

    def update_movement(self, movement : Movement):
        self.cursor.execute(
            "UPDATE player_movement SET reactions={}, balance={}, acceleration={}, sprint_speed={}, agility={}, player_id={} WHERE (movement_id={})".format(*movement.get_movement("update")))
        self.connection.commit()

    def delete_movement(self, movement_id):
        self.cursor.execute(
            "DELETE FROM player_movement WHERE movement_id={}".format(movement_id))
        self.connection.commit()

    def get_movement(self, movement_id):
        self.cursor.execute(
            "SELECT * FROM player_movement WHERE movement_id={}".format(movement_id))
        results = self.cursor.fetchone()
        return results

    def get_player_power_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_power WHERE player_id='{}'".format(player_id))
      player_power=self.cursor.fetchall()
      return player_power

    def get_player_movement_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_movement WHERE player_id='{}'".format(player_id))
      player_movement=self.cursor.fetchall()
      return player_movement

# -------------SILA----------------------------------

    # player_goalkeeping

    def insert_mentality(self, mentality):
        self.cursor.execute("INSERT INTO player_mentality(player_id, aggression, interceptions, positioning, vision, penalties, composure) VALUES(%s, %s, %s, %s, %s, %s, %s)", (
            mentality.player_id, mentality.aggression, mentality.interceptions,
            mentality.positioning, mentality.vision, mentality.penalties,
            mentality.composure))

        # since mentality_id is auto-increment, pgadmin will determine it. For keeping mentality_id in the mentality class
        # we should set it by getter and setter methods assuming player_id and mentality_id are always the same (?)
        # or keep mentality_count as a global variable and increment with insert and decrement with delete operation

        # mentality.set_mentality_id(mentality.get_player_id)
        self.connection.commit()
    
    def update_mentality(self, mentality):
        #if not all values are to be changed, dont change those in mentality object
        self.cursor.execute("UPDATE player_mentality SET aggression=%s, interceptions=%s, positioning=%s, vision=%s, "
                            "penalties=%s, composure=%s WHERE (mentality_id = %s)", (mentality.aggression, mentality.interceptions,
                                                                               mentality.positioning, mentality.vision,
                                                                               mentality.penalties, mentality.composure,
                                                                               mentality.mentality_id,
                                                                               ))
        self.connection.commit()

    def delete_mentality(self, mentality_id):
        self.cursor.execute(
            "DELETE FROM player_mentality WHERE mentality_id=%s", (mentality_id,))
        self.connection.commit()
    
    def get_player_mentality(self, mentality_id):
        statement = """SELECT * FROM player_mentality WHERE (mentality_id={})""".format(mentality_id)
        self.cursor.execute(statement, (mentality_id,))
        mentality = self.cursor.fetchone()
        return mentality

    #search and get player
    def get_player_name(self, player_name):
        self.cursor.execute(
            "SELECT * FROM player WHERE player_name ILIKE %s", ('%' + player_name + '%',))
        results = self.cursor.fetchall()
        return results

    def get_team_name(self, team_name):
        self.cursor.execute(
            "SELECT * FROM team WHERE team_name ILIKE %s", ('%' + team_name + '%',))
        results = self.cursor.fetchall()
        return results
    
    # player_goalkeeping
    def insert_goalkeeping(self, goalkeeping):
        self.cursor.execute("INSERT INTO player_goalkeeping(player_id, diving, handling, kicking, positioning, reflexes) VALUES(%s, %s, %s, %s, %s, %s)", (
            goalkeeping.player_id, goalkeeping.diving,
            goalkeeping.handling, goalkeeping.kicking,
            goalkeeping.positioning, goalkeeping.reflexes))
        self.connection.commit()

    def update_goalkeeping(self, goalkeeping):
        self.cursor.execute("UPDATE player_goalkeeping SET diving=%s, handling=%s, kicking=%s, positioning=%s, "
                            "reflexes=%s WHERE (goalkeeping_id = %s)", (
                                goalkeeping.diving,
                                goalkeeping.handling, goalkeeping.kicking,
                                goalkeeping.positioning, goalkeeping.reflexes, goalkeeping.goalkeeping_id, ))
        self.connection.commit()

    def get_player_goalkeeping(self, goalkeeping_id):
        statement = """SELECT * FROM player_goalkeeping WHERE (goalkeeping_id={})""".format(goalkeeping_id)
        self.cursor.execute(statement, (goalkeeping_id,))
        goalkeeping = self.cursor.fetchone()
        return goalkeeping

    def delete_goalkeeping(self, goalkeeping_id):
        self.cursor.execute(
            "DELETE FROM player_goalkeeping WHERE goalkeeping_id=%s", (goalkeeping_id,))
        self.connection.commit()
                                                              

  # -------------DARIA----------------------------------     
  
    #team
    def insert_team(self,team):
      self.cursor.execute("""INSERT INTO team(team_name,league,overall,attack,midfield,defense,international_prestige,domestic_prestige,transfer_budget) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (team.team_name,team.league,team.overall,
            team.attack,team.midfield,team.defense,team.international_prestige,
            team.domestic_prestige,team.transfer_budget))
      self.connection.commit()
      
    def update_team(self,league,overall,attack,midfield,defense,international_prestige,domestic_prestige,transfer_budget,team_id):
      statement="""UPDATE team SET league=%s , overall=%s , attack=%s , midfield=%s , defense=%s , international_prestige=%s , domestic_prestige=%s , transfer_budget=%s WHERE team_id=%s"""
      self.cursor.execute(statement,(league,overall,attack,midfield,defense,
                                     international_prestige,domestic_prestige,transfer_budget,team_id))
      self.connection.commit()
      
    def delete_team(self,team_id):
      statement="""DELETE FROM team WHERE (team_id='{}')""".format(team_id)
      self.cursor.execute(statement,(team_id))
      self.connection.commit()
      
    def get_team(self,team_id):
      statement="""SELECT FROM team WHERE team_id=%s"""
      self.cursor.execute(statement,(team_id))
      team=self.cursor.fetchone()
      self.connection.commit()
      return team
    
      
    #team_tactics
    def insert_team_tactics(self,team_tactics):
      statement="""INSERT INTO team_tactics(team_id,defensive_style,team_width,depth,offensive_style,width,players_in_box,corners,freekicks) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
      self.cursor.execute(statement,(team_tactics.team_id,team_tactics.defensive_style,team_tactics.team_width,team_tactics.depth,team_tactics.offensive_style,
      team_tactics.width,team_tactics.players_in_box,team_tactics.corners,team_tactics.freekicks))
      self.connection.commit()
    
    def update_team_tactics(self,team_tactics):
      statement="""UPDATE team_tactics SET defensive_style=%s,team_width=%s,depth=%s,offensive_style=%s,width=%s,players_in_box=%s,corners=%s,freekicks=%s WHERE (tactic_id=%s)"""
      self.cursor.execute(statement,(team_tactics.defensive_style,team_tactics.team_width,team_tactics.depth,team_tactics.offensive_style,
      team_tactics.width,team_tactics.players_in_box,team_tactics.corners,team_tactics.freekicks,team_tactics.tactic_id))
      self.connection.commit()
    
    def delete_team_tactics(self,tactic_id):
      statement="""DELETE FROM team_tactics WHERE (tactic_id='{}')""".format(tactic_id)
      self.cursor.execute(statement,(tactic_id))
      self.connection.commit()
    
    def get_team_tactics(self,tactic_id):
      statement="""SELECT * FROM team_tactics WHERE tactic_id=%s"""
      self.cursor.execute(statement,(tactic_id,))
      team_tactics=self.cursor.fetchone()
      self.connection.commit()
      return team_tactics
    
    def view_teams(self):
      self.cursor.execute('SELECT * FROM team ORDER BY team_id;')
      teams=self.cursor.fetchall()
      return teams

    def view_players(self):
      self.cursor.execute('SELECT * FROM player ORDER BY player_id;')
      players=self.cursor.fetchall()
      return players

    def view_all_tactics(self):
      self.cursor.execute('SELECT * FROM team_tactics;')
      tactics=self.cursor.fetchall()
      return tactics

    def view_leagues(self):
      self.cursor.execute('SELECT DISTINCT league FROM team;')
      leagues=self.cursor.fetchall()
      return leagues 

    def view_teams_of_league(self,league):
      self.cursor.execute("SELECT * FROM team WHERE (league='{}')".format(league))
      teams=self.cursor.fetchall()
      return teams

    def view_players_of_team(self,team_id):
        
      self.cursor.execute("SELECT * FROM player WHERE team_id='{}'".format(team_id) )
      players=self.cursor.fetchall()
      print(players)
      return players

    def view_tactics(self,team_id):
      self.cursor.execute("SELECT * FROM team_tactics WHERE team_id='{}'".format(team_id))
      tactic=self.cursor.fetchall()
      return tactic

    def get_attacking_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_attacking WHERE player_id='{}'".format(player_id))
      attacking=self.cursor.fetchall()
      return attacking
    
    def get_player_profile_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_profile WHERE player_id='{}'".format(player_id))
      player_profile=self.cursor.fetchall()
      return player_profile

    def get_player_skills_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_skills WHERE player_id='{}'".format(player_id))
      player_skills=self.cursor.fetchall()
      return player_skills

    def get_player_goalkeeping_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_goalkeeping WHERE player_id='{}'".format(player_id))
      player_goalkeeping=self.cursor.fetchall()
      return player_goalkeeping

    def get_player_mentality_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_mentality WHERE player_id='{}'".format(player_id))
      player_mentality=self.cursor.fetchall()
      return player_mentality

    def get_player_power_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_power WHERE player_id='{}'".format(player_id))
      player_power=self.cursor.fetchall()
      return player_power

    def get_player_movement_p(self,player_id):
      self.cursor.execute("SELECT * FROM player_movement WHERE player_id='{}'".format(player_id))
      player_movement=self.cursor.fetchall()
      return player_movement
