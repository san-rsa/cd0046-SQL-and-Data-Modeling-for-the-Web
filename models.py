from email.policy import default
from sqlalchemy import ARRAY
from flask_sqlalchemy import SQLAlchemy
from enum import unique
import datetime

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    genres = db.Column(db.ARRAY(db.String())) 
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link  = db.Column(db.String()) 
    seeking_talent = db.Column(db.String()) # can't edit in boolean "not a boolean value true" 
    seeking_description = db.Column(db.String()) 
    
    # shows = db.relationship('show', backref='venue', lazy=True)
    

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link  = db.Column(db.String())  
    seeking_venue = db.Column(db.String()) # can't edit in boolean "not a boolean value true"
    seeking_description  = db.Column(db.String()) 
    
    # shows = db.relationship('show', backref='artist', lazy=True)
    
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False)
