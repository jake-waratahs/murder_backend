from application import db

kills = db.Table("kills", 
    db.Column("game_id", db.Integer, db.ForeignKey("game.id")),
    db.Column("killer_id", db.Integer, db.ForeignKey("player.id")),
    db.Column("killed_id", db.Integer, db.ForeignKey("player.id")),
    db.Column("time", db.DateTime)
    )