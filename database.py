import psycopg2
from classes import *


class Database:
    def __init__(self,hostname='localhost',user='postgres',password='postgres',port=5432,dbname='Fifa'):
        self.hostname = hostname
        self.user = user
        self.password = password
        self.port = port
        self.dbname = dbname

    # player_image_url?
    def insert_player(self,player):
        with psycopg2.connect(host = self.hostname, dbname= self.dbname, user=self.user, password=self.password, port=self.port) as connection:
            with connection.cursor() as cursor:
                statement = """INSERT INTO player(player_name,date_of_birth,height,weight,overall_rating,potential_rating,best_position,best_overall_rating,value,wage,player_image_url,team_id,nationality) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(statement,(player.player_name,player.date_of_birth,player.height,player.weight,player.overall_rating,player.potential_rating,player.best_position,player.best_overall_rating,player.value,player.wage,player.player_image_url,player.team_id,player.nationality))
                cursor.close()

    # can player_name be updated or not?
    def update_player(self,player):
        with psycopg2.connect(host = self.hostname, dbname= self.dbname, user=self.user, password=self.password, port=self.port) as connection:
            with connection.cursor() as cursor:
                statement = """UPDATE player SET date_of_birth=%s, height=%s, weight=%s, overall_rating=%s, potential_rating=%s, best_position=%s, best_overall_rating=%s, value=%s, wage=%s, player_image_url=%s, team_id=%s, nationality=%s"""
                cursor.execute(statement,(player.date_of_birth,player.height,player.weight,player.overall_rating,player.potential_rating,player.best_position,player.best_overall_rating,player.value,player.wage,player.player_image_url,player.team_id,player.nationality))
                cursor.close()

    def delete_player(self,player_id):
        with psycopg2.connect(host = self.hostname, dbname= self.dbname, user=self.user, password=self.password, port=self.port) as connection:
            with connection.cursor() as cursor:
                statement = """DELETE FROM player WHERE (player_id=%s)"""
                cursor.execute(statement,(player_id))
                cursor.close()
    
    def insert_player_attacking(self,player_attacking):
        with psycopg2.connect(host = self.hostname, dbname= self.dbname, user=self.user, password=self.password, port=self.port) as connection:
            with connection.cursor() as cursor:
                statement = """INSERT INTO player_attacking(player_id,crossing,finishing,heading_accuracy,short_passing,volleys) VALUES(%s, %s, %s, %s, %s, %s)"""
                cursor.execute(statement,(player_attacking.player_id,player_attacking.crossing,player_attacking.finishing,player_attacking.heading_accuracy,player_attacking.short_passing,player_attacking.volleys))
                cursor.close()

    # can player_id be updated or not?    
    def update_player_attacking(self,player_attacking):
        with psycopg2.connect(host = self.hostname, dbname= self.dbname, user=self.user, password=self.password, port=self.port) as connection:
            with connection.cursor() as cursor:
                statement = """UPDATE player_attacking SET crossing=%s, finishing=%s, heading_accuracy=%s, short_passing=%s, volleys=%s"""
                cursor.execute(statement,(player_attacking.crossing,player_attacking.finishing,player_attacking.heading_accuracy,player_attacking.short_passing,player_attacking.volleys))
                cursor.close()

    def delete_player_attacking(self,player_attacking_id):
        with psycopg2.connect(host = self.hostname, dbname= self.dbname, user=self.user, password=self.password, port=self.port) as connection:
            with connection.cursor() as cursor:
                statement = """DELETE FROM player_attacking WHERE attacking_id=?"""
                cursor.execute(statement,(player_attacking_id))
                cursor.close()

    def get_player(self,player_id):
        with psycopg2.connect(host = self.hostname, dbname= self.dbname, user=self.user, password=self.password, port=self.port) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT FROM player WHERE (player_id=%s)"""
                cursor.execute(statement,(player_id))
                player = cursor.fetchone()
                cursor.close()
                return player

    def get_player_attacking(self,player_attacking_id):
        with psycopg2.connect(host = self.hostname, dbname= self.dbname, user=self.user, password=self.password, port=self.port) as connection:
            with connection.cursor() as cursor:
                statement = """SELECT FROM player WHERE (player_attacking_id=%s)"""
                cursor.execute(statement,(player_attacking_id))
                player_attacking = cursor.fetchone()
                cursor.close()
                return player_attacking
