from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class URLRange(db.Model):
    __tablename__ = 'url_range'
    id = db.Column(db.Integer, primary_key=True)
    start_range = db.Column(db.Integer, nullable=False)
    end_range = db.Column(db.Integer, nullable=False)
    current_number = db.Column(db.Integer, nullable=False)


class URLDetails(db.Model):
    __tablename__ = 'url_details'
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(20), nullable=False)
    original_url = db.Column(db.String(1000), nullable=False)
    no_of_clicks = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(250), nullable=False)


class Mapping(db.Model):
    __tablename__ = 'mapping_code'
    mapping_number = db.Column(db.String(6), primary_key = True)
    mapping_character = db.Column(db.String(1), nullable = False)

