from web import db

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, unique=False, nullable=False)
    y = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f"{self.id}. Point ({self.x}, {self.y})"

