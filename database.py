import psycopg2
from classes import *


class Database:
    def __init__(self,hostname,user,password,port,dbname):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.port = port
        self.dbname = dbname

    # player_image_url?
    def insert_player(self,player):
        with psycopg2.connect(self.hostname, self.dbname, self.user, self.password, self.port) as connection:
            with connection.cursor() as cursor:
                statement = """INSERT INTO player VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(statement,(player.player_id,player.player_name,player.date_of_birth,player.heigth,player.weigth,player.overall_rating,player.potential_rating,player.best_position,player.best_overall_rating,player.value,player.wage,player.player_image_url,player.team_id,player.nationality))
                cursor.close()

    # can player_name be updated or not?
    def update_player(self,player):
        with psycopg2.connect(self.hostname, self.dbname, self.user, self.password, self.port) as connection:
            with connection.cursor() as cursor:
                statement = """UPDATE player SET date_of_birth=?, heigth=?, weigth=?, overall_rating=?, potential_rating=?, best_position=?, best_overall_rating=?, value=?, wage=?, player_image_url=?, team_id=?, nationality=?"""
                cursor.execute(statement,(player.date_of_birth,player.heigth,player.weigth,player.overall_rating,player.potential_rating,player.best_position,player.best_overall_rating,player.value,player.wage,player.player_image_url,player.team_id,player.nationality))
                cursor.close()

    def delete_player(self,player):
        with psycopg2.connect(self.hostname, self.dbname, self.user, self.password, self.port) as connection:
            with connection.cursor() as cursor:
                statement = """DELETE FROM player WHERE player_id=?"""
                cursor.execute(statement,(player.player_id))
                cursor.close()
    
    def insert_player_attacking(self,player_attacking):
        with psycopg2.connect(self.hostname, self.dbname, self.user, self.password, self.port) as connection:
            with connection.cursor() as cursor:
                statement = """INSERT INTO player_attacking VALUES(?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(statement,(player_attacking.attacking_id,player_attacking.player_id,player_attacking.crossing,player_attacking.finishing,player_attacking.heading_accuracy,player_attacking.short_passing,player_attacking.volleys))
                cursor.close()

    # can player_id be updated or not?    
    def update_player_attacking(self,player_attacking):
        with psycopg2.connect(self.hostname, self.dbname, self.user, self.password, self.port) as connection:
            with connection.cursor() as cursor:
                statement = """UPDATE player_attacking SET crossing=?, finishing=?, heading_accuracy=?, short_passing=?, volleys=?"""
                cursor.execute(statement,(player_attacking.crossing,player_attacking.finishing,player_attacking.heading_accuracy,player_attacking.short_passing,player_attacking.volleys))
                cursor.close()

    def delete_player_attacking(self,player_attacking):
        with psycopg2.connect(self.hostname, self.dbname, self.user, self.password, self.port) as connection:
            with connection.cursor() as cursor:
                statement = """DELETE FROM player_attacking WHERE attacking_id=?"""
                cursor.execute(statement,(player_attacking.attacking_id))
                cursor.close()
