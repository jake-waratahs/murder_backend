from application import db
from application.model import Player

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    winner_id = db.Column(db.Integer, db.ForeignKey("player.id"))

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def serialize(self):
        winner = Player.query.filter_by(id=self.winner_id).first()
        winner_name = None
        
        if winner is not None:
            winner_name = winner.full_name

        return {
            "id": self.id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "winner": winner_name
        }