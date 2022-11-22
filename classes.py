
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
        