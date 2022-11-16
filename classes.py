
class Player:
    def __init__(self, player_id):
        self.player_id = player_id


class Goalkeeping:
    def __init__(self, goalkeeping_id, diving, handling, kicking, positioning, reflexes, player_id):
        self.goalkeeping_id = goalkeeping_id
        self.diving = diving
        self.handling = handling
        self.kicking = kicking
        self.positioning = positioning
        self.reflexes = reflexes
        self.player_id = player_id


class Mentality:
    def __init__(self, mentality_id, aggression, interceptions, positioning, vision, penalties, composure, player_id):
        self.mentality_id = mentality_id
        self.aggression = aggression
        self.interceptions = interceptions
        self.positioning = positioning
        self.vision = vision
        self.penalties = penalties
        self.composure = composure
        self.player_id = player_id
