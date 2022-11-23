from classes import *
import psycopg2 as dbapi

#mentality_count = 19002

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.dbname = 'Fifa'
        self.user = 'postgres'
        self.password = 'postgres'
        self.connection = dbapi.connect(host=self.host, database=self.dbname, user=self.user, password=self.password)
        self.cursor = self.connection.cursor()

   

    # player_mentality
    def insert_mentality(self, mentality):
        self.cursor.execute("INSERT INTO player_mentality VALUES('%s', '%s','%s', '%s', '%s', '%s', '%s')", (
                                                                    mentality.player_id, mentality.aggression, mentality.interceptions, 
                                                                    mentality.positioning, mentality.vision, mentality.penalties,
                                                                    mentality.composure))
        
        # since mentality_id is auto-increment, pgadmin will determine it. For keeping mentality_id in the mentality class
        # we should set it by getter and setter methods assuming player_id and mentality_id are always the same (?)
        # or keep mentality_count as a global variable and increment with insert and decrement with delete operation
        
        #mentality.set_mentality_id(mentality.get_player_id)
        self.connection.commit()

    def update_mentality(self, mentality):
        self.cursor.execute("UPDATE player_mentality SET aggression='%s', interceptions='%s', positioning='%s', vision='%s', "
                            "penalties='%s', composure='%s', player_id='%s'", (mentality.player_id, mentality.aggression, mentality.interceptions,
                                                                      mentality.positioning, mentality.vision,
                                                                      mentality.penalties, mentality.composure,
                                                                      ))
        self.connection.commit()

    def delete_mentality(self, mentality_id):
        self.cursor.execute("DELETE FROM player_mentality WHERE mentality_id='%s'", (mentality_id,))
        self.connection.commit()

    # player_goalkeeping
    def insert_goalkeeping(self, goalkeeping):
        self.cursor.execute("INSERT INTO player_goalkeeping VALUES('%s', '%s','%s', '%s', '%s', '%s', '%s')", (
                                                                goalkeeping.player_id, goalkeeping.diving, 
                                                                goalkeeping.handling, goalkeeping.kicking, 
                                                                goalkeeping.positioning, goalkeeping.reflexes))
        self.connection.commit()

    def update_goalkeeping(self, goalkeeping):
        self.cursor.execute("UPDATE player_goalkeeping SET aggression='%s', interceptions='%s', positioning'%s', vision='%s', "
                            "penalties='%s', composure='%s', player_id='%s'", (
                                                                goalkeeping.player_id, goalkeeping.diving, 
                                                                goalkeeping.handling, goalkeeping.kicking,
                                                                goalkeeping.positioning, goalkeeping.reflexes, ))
        self.connection.commit()

    def delete_goalkeeping(self, goalkeeping_id):
        self.cursor.execute("DELETE FROM player_goalkeeping WHERE goalkeeping_id='%s'", (goalkeeping_id,))
        self.connection.commit()


    # player_power
    def insert_power(self, power):
        self.cursor.execute("INSERT INTO player_power VALUES('%s', '%s','%s', '%s', '%s', '%s', '%s')", power.get_power())
        self.connection.commit()

    def update_power(self, power):
        self.cursor.execute("UPDATE player_power SET strength='%s', long_shots='%s', shot_power'%s', jumping='%s', stamina='%s', player_id='%s'", power.get_power())
        self.connection.commit()

    def delete_power(self, power_id):
        self.cursor.execute("DELETE FROM player_power WHERE power_id='%s'", (power_id,))
        self.connection.commit()

    # player_movement
    def insert_movement(self, movement):
        self.cursor.execute("INSERT INTO player_movement VALUES('%s', '%s','%s', '%s', '%s', '%s', '%s')", movement.get_movement())
        self.connection.commit()

    def update_movement(self, movement):
        self.cursor.execute("UPDATE player_movement SET reactions_id='%s', balance='%s', acceleration'%s', sprint_speed='%s', agility='%s', player_id='%s'", movement.get_movement())
        self.connection.commit()

    def delete_movement(self, movement_id):
        self.cursor.execute("DELETE FROM player_movement WHERE movement_id='%s'", (movement_id,))
        self.connection.commit()
    