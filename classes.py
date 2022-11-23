class Player:
    def __init__(self, player_id, player_name, date_of_birth, height, weight, overall_rating,
                 potential_rating, best_position, best_overall_rating, value, wage,
                 player_image_url, team_id, nationality):

        self.player_id = player_id
        self.player_name = player_name
        self.date_of_birth = date_of_birth
        self.height = height
        self.weight = weight
        self.overall_rating = overall_rating
        self.potential_rating = potential_rating
        self.best_position = best_position
        self.best_overall_rating = best_overall_rating
        self.value = value
        self.wage = wage
        self.player_image_url = player_image_url
        self.team_id = team_id
        self.nationality = nationality


class PlayerAttacking:
    def __init__(self, attacking_id, player_id, crossing, finishing,
                 heading_accuracy, short_passing, volleys):
        self.attacking_id = attacking_id
        self.player_id = player_id
        self.crossing = crossing
        self.finishing = finishing
        self.heading_accuracy = heading_accuracy
        self.short_passing = short_passing
        self.volleys = volleys

class Goalkeeping:
    def __init__(self, goalkeeping_id, player_id, diving, handling, kicking, positioning, reflexes):
        self.goalkeeping_id = goalkeeping_id
        self.player_id = player_id
        self.diving = diving
        self.handling = handling
        self.kicking = kicking
        self.positioning = positioning
        self.reflexes = reflexes       
    
    def set_goalkeeping_id(self, goalkeeping_id):
        self.goalkeeping_id = goalkeeping_id

    def get_player_id(self):
        return self.player_id


class Mentality:
    def __init__(self, mentality_id, player_id, aggression, interceptions, positioning, vision, penalties, composure):
        self.mentality_id = mentality_id
        self.player_id = player_id
        self.aggression = aggression
        self.interceptions = interceptions
        self.positioning = positioning
        self.vision = vision
        self.penalties = penalties
        self.composure = composure
    
    def set_mentality_id(self, mentality_id):
        self.mentality_id = mentality_id

    def get_player_id(self):
        return self.player_id

class Power:
    def __init__(self, power_id, strength, long_shots, shot_power, jumping, stamina, player_id):
        self.power_id = power_id
        self.strength = strength
        self.long_shots = long_shots
        self.shot_power = shot_power
        self.jumping = jumping
        self.stamina = stamina
        self.player_id = player_id

    
    def set_power_id(self, power_id):
        self.power_id = power_id

    def get_player_id(self):
        return self.player_id


class Movement:
    def __init__(self, movement_id, reactions_id, balance, acceleration, sprint_speed, agility, player_id):
        self.movement_id = movement_id
        self.reactions_id = reactions_id
        self.balance = balance
        self.acceleration = acceleration
        self.sprint_speed = sprint_speed
        self.agility = agility
        self.player_id = player_id
    
    def set_movement_id(self, movement_id):
        self.movement_id = movement_id

    def get_player_id(self):
        return self.player_id