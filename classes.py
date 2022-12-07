
class Player:
    def __init__(self, player_name, date_of_birth, height, weight, overall_rating,
                 potential_rating, best_position, best_overall_rating, value, wage,
                 player_image_url, team_id, nationality, player_id=None):

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
    def __init__(self, player_id, crossing, finishing, heading_accuracy, short_passing, volleys, attacking_id=None):
        self.attacking_id = attacking_id
        self.player_id = player_id
        self.crossing = crossing
        self.finishing = finishing
        self.heading_accuracy = heading_accuracy
        self.short_passing = short_passing
        self.volleys = volleys


class player_profile:
    def __init__(self, profile_id, skill_moves, international_reputations, work_rate, body_type, preferred_foot, weak_foot, player_id):
        self.profile_id = profile_id
        self.skill_moves = skill_moves
        self.international_reputations = international_reputations
        self.work_rate = work_rate
        self.body_type = body_type
        self.preferred_foot = preferred_foot
        self.weak_foot = weak_foot
        self.player_id = player_id


class player_skills:
    def __init__(self, skill_id, dribbling, curve, fk_accuracy, long_passing, ball_control, player_id):
        self.skill_id = skill_id
        self.curve = curve
        self.dribbling = dribbling
        self.fk_accuracy = fk_accuracy
        self.long_passing = long_passing
        self.ball_control = ball_control
        self.player_id = player_id


class Goalkeeping:
    def __init__(self, goalkeeping_id, diving, handling, kicking, positioning, reflexes,player_id):
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
    def __init__(self, mentality_id, aggression, interceptions, positioning, vision, penalties, composure,  player_id):
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

    def get_power(self):
        return(self.strength, self.long_shots, self.shot_power, self.jumping, self.stamina, self.player_id)


class Movement:
    def __init__(self, movement_id, reactions_id, balance, acceleration, sprint_speed, agility, player_id ):
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

    def get_movement(self):
        return(self.reactions_id, self.balance, self.acceleration, self.sprint_speed, self.agility, self.player_id)
