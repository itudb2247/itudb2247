
class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    

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
