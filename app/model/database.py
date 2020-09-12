from app.control import generate_id, get_date
from app.model import db

class Audience(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Checkout(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    date = db.Column(db.DateTime)
    audience_id = db.Column(db.String(50))

    def __init__(self, audience_id):
        self.id = generate_id()
        self.date = get_date()
        self.audience_id = audience_id
