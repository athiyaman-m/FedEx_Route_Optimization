from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(100))
    end = db.Column(db.String(100))
    distance_km = db.Column(db.Float)
    emissions = db.Column(db.Float)
    traffic = db.Column(db.Text)
    weather = db.Column(db.Text)
