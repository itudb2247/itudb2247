from classes import *
import psycopg2 as dbapi


class Database:
    def __init__(self, host, dbname, user, password, port):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.connection = dbapi.connect(self.host, self.dbname, self.user, self.password, self.port)
        self.cursor = self.connection.cursor()

    # player_mentality
    def insert_mentality(self, mentality):
        self.cursor.execute("INSERT INTO player_mentality VALUES(?, ?, ?, ?, ?, ?, ?)", (
            mentality.aggression, mentality.interceptions, mentality.positioning, mentality.vision, mentality.penalties,
            mentality.composure, mentality.player_id))
        self.connection.commit()

    def update_mentality(self, mentality):
        self.cursor.execute("UPDATE player_mentality SET aggression=?, interceptions=?, positioning=?, vision=?, "
                            "penalties=?, composure=?, player_id=?", (mentality.aggression, mentality.interceptions,
                                                                      mentality.positioning, mentality.vision,
                                                                      mentality.penalties, mentality.composure,
                                                                      mentality.player_id))
        self.connection.commit()

    def delete_mentality(self, mentality_id):
        self.cursor.execute("DELETE FROM player_mentality WHERE mentality_id=?", (mentality_id))
        self.connection.commit()

    # player_goalkeeping
    def insert_goalkeeping(self, goalkeeping):
        self.cursor.execute("INSERT INTO player_goalkeeping VALUES(?, ?, ?, ?, ?, ?, ?)", (
            goalkeeping.diving, goalkeeping.handling, goalkeeping.kicking, goalkeeping.positioning,
            goalkeeping.reflexes, goalkeeping.player_id))
        self.connection.commit()

    def update_goalkeeping(self, goalkeeping):
        self.cursor.execute("UPDATE player_goalkeeping SET aggression=?, interceptions=?, positioning=?, vision=?, "
                            "penalties=?, composure=?, player_id=?",
                            (goalkeeping.diving, goalkeeping.handling, goalkeeping.kicking, goalkeeping.positioning,
                             goalkeeping.reflexes, goalkeeping.player_id))
        self.connection.commit()

    def delete_goalkeeping(self, goalkeeping_id):
        self.cursor.execute("DELETE FROM player_goalkeeping WHERE goalkeeping_id=?", (goalkeeping_id))
        self.connection.commit()
