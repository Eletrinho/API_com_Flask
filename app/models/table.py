from app import db

class FilmesDB(db.Model):
    __tablename__ = "filmes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    year = db.Column(db.Integer)
    profit = db.Column(db.Float)

    def __init__(self, name, year, profit=None):
        self.name = name
        self.year = year
        self.profit = profit

    def get(self):
        return {"id": self.id, "name": self.name, "year": self.year, "profit": self.profit}

    def update(self, **kwargs):
        self.name = kwargs['name']
        self.year = kwargs['year']
        self.profit = kwargs['profit']