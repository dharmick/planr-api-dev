from database import db
from sqlalchemy.dialects.postgresql import JSON


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Cities(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

class UserRatings(db.Model):
    __tablename__ = 'user_ratings'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users")

    poi_id = db.Column(db.Integer, db.ForeignKey('pois.id'))
    poi = db.relationship("Pois")

    rating = db.Column(db.Float)


class Pois(db.Model):
    __tablename__ = 'pois'

    id = db.Column(db.Integer, primary_key=True)

    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship("Cities")

    name = db.Column(db.String(50))
    opening_time = db.Column(db.Float)
    closing_time = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    time_to_spend = db.Column(db.Float)
    category = db.Column(db.String(15))
    average_rating = db.Column(db.Float)


