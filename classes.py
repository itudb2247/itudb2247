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
       