import psycopg2 as dbapi
from classes import *
class Database:
    def init(self, host, dbname, user, password, port):
        #check if database exists
        self.host = host
        self.db_name = dbname
        self.user = user
        self.password = password
        self.port = port
        self.connection = dbapi.connect(self.host, self.dbname, self.user, self.password, self.port)
        self.cursor = self.connection.cursor()

    def insert_player_profile(self, player_profile):
        self.cursor.execute("INSERT INTO player_profile VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (player_profile.profile_id,player_profile.skill_moves,player_profile.international_reputations, player_profile.work_rate, player_profile.body_type, player_profile.preferred_foot, player_profile.weak_foot, player_profile.player_id))
        self.conn.commit()
    def delete_player_profile(self, profile_id):
        self.cursor.execute("DELETE FROM player_profile WHERE profile_id=?", (profile_id,))
        self.conn.commit()
    def insert_player_profile(self, player_skills):
        self.cursor.execute("INSERT INTO player_skills VALUES(?, ?, ?, ?, ?, ?, ?)",
                            (player_skills.skill_id,player_skills.dribbling,player_skills.curve,player_skills.fk_accuracy,player_skills.long_passing,player_skills.ball_control,player_skills.player_id))
        self.conn.commit()
    def delete_player_profile(self, skill_id):
        self.cursor.execute("DELETE FROM player_skills WHERE skill_id=?", (skill_id,))
        self.conn.commit()