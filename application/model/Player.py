from application import db
from .Kills import kills

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zid = db.Column(db.String(8))
    full_name = db.Column(db.String(255))
    admin = db.Column(db.Boolean)
    
    # Relationships
    winnings = db.relationship("Game", backref="winner",
        lazy="dynamic")
    kills = db.relationship("Player", secondary=kills,
        primaryjoin=id==kills.c.killer_id,
        secondaryjoin=id==kills.c.killed_id)


    def __init__(self, zid, full_name, admin):
        self.zid = zid
        self.full_name = full_name
        self.admin = admin

    def serialize(self):
        return {
            "id": self.id,
            "zid": self.zid,
            "name": self.full_name,
            "admin": self.admin,
            "wins": len(self.winnings.all()),
            "kills": len(self.kills)
        }