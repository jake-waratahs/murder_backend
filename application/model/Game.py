from application import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    winner_id = db.Column(db.Integer, db.ForeignKey("player.id"))

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date