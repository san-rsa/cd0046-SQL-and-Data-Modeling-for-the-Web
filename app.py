#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from ast import Str
from distutils.log import error
from ftplib import error_reply
from importlib.util import LazyLoader
from itertools import count
import json
from os import name
from unittest import result
from urllib import response
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from jinja2.utils import markupsafe
# from matplotlib import artist
from sqlalchemy import ARRAY
markupsafe.Markup()
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import  *
from models import Show , Artist, Venue, db
import sys

import config
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)

app.config.from_object(config)
db.init_app(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  # if isinstance(value, str):
  #       date = dateutil.parser.parse(value)
  # else:
  #       date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
   return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  locations = Venue.query.distinct(Venue.city, Venue.state).all()
  data = []
  for venue in locations:
    li = {}
    li['city'] = venue.city
    li['state'] = venue.state

    venues = []

    info = Venue.query.filter(Venue.state == venue.state, Venue.city==venue.city).all()

    time = datetime.now()
    for thisVenue in info:
      currentVenue = ({
        'id' : thisVenue.id,
        'name' : thisVenue.name,
        'num_upcoming_shows' : db.session.query(Show).join(Venue).filter(Show.venue_id==thisVenue.id, Show.start_time> time).all()
 # NOTE all venue must have start time if not there will be an error  
      
      })

      venues.append(currentVenue)
    li['venues'] = venues
    data.append(li)  




      
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  response={}
  data = []
  text = request.form['search_term']
  

  try:
      
    search_result = db.session.query(Venue.id, Venue.name).filter_by(name=text).all()

    for result in search_result:
        data.append({
          "id": Venue.id,
          "name": result.name
        })
        response = {
          "data":data,
          "count": len(search_result)
        }

  except:
    error = True
    print(sys.exc_info)
    flash('venue can\'t be found please try again or use different a name ' )
    return render_template('pages/home.html')

  finally:
 
   return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data = Venue.query.get(venue_id)
  
    
  upcoming_shows_query =db.session.query(Show).join(Venue).filter(Show.artist_id==venue_id).filter(Show.start_time>datetime.now()).all()
  past_shows_query = past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==venue_id).filter(Show.start_time>datetime.now()).all()

  upcoming_shows= []

  past_shows= []

  for shows in upcoming_shows_query:
    upcoming_shows.append({
   
      "venue_id" : shows.id,
      "venue_name" : shows.name,
      "venue_image_link" : shows.image_link,
      "start_time" : Show.start_time
    })
  for shows in past_shows_query:
    upcoming_shows.append({
   
      "venue_id" : shows.id,
      "venue_name" : shows.name,
      "venue_image_link" : shows.image_link,
      "start_time" : Show.start_time
    })






  return render_template('pages/show_venue.html', venue=data, upcoming_shows=upcoming_shows, past_shows=past_shows)
# #  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  error = False
  new = request.form.get

  # TODO: insert form data as a new Venue record in the db, instead
  try:
      venue = Venue(

         name=form.name.data,
         city=form.city.data,
         state=form.state.data,
         address = form.address.data,
         phone=form.phone.data,
         genres=form.genres.data,
         facebook_link=form.facebook_link.data,
         image_link=form.image_link.data,
         website_link=form.website_link.data,
         seeking_talent=form.seeking_talent.data,
         seeking_description=form.seeking_description.data

  

      )

      db.session.add(venue)
      db.session.commit()
  except:
      db.session.rollback()
      error = True
      print(sys.exc_info())

  finally:
      print(sys.exc_info())

      db.session.close()

  if error: 
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    print(sys.exc_info())
 
   # return render_template('forms/new_venue.html', form=form)
  # on successful db insert, flash success
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')  

    print(sys.exc_info())

  # TODO: modify data to be the data object returned from db insertion

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  venue = db.session.query.get(Venue.id).first()

  db.session.delete(venue)
  db.session.cpmmit()
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
    
    data = Artist.query.all()

    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  error = False
  response = {}
  data = []
  text = request.form['search_term']
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  search_artist = db.session.query(Artist.id, Artist.name).filter_by(name=text).all()

  try:
     for result in search_artist:
      data.append({
      "id": result.id,
      "name": result.name
    })
      response = {
      "data":data,
      "count": len(search_artist)
    }
  except:
    error = True
    print(sys.exc_info)
    flash('artist can\'t be found please try again or use different a name ' )
    return render_template('pages/home.html')

  finally:



   return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

  

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id


  artist = Artist.query.get(artist_id)

  upcoming_shows_query =db.session.query(Venue).join(Show).filter(Show.artist_id==Venue.id).filter(Show.start_time>datetime.now()).all()
  past_shows_query =  db.session.query(Venue).join(Show).filter(Show.artist_id==Venue.id).filter(Show.start_time>datetime.now()).all()

  upcoming_shows= []

  past_shows= []

  for shows in upcoming_shows_query:
    upcoming_shows.append({
   
      "venue_id" : shows.id,
      "venue_name" : shows.name,
      "venue_image_link" : shows.image_link,
      "start_time" : Show.start_time
    })
  for shows in past_shows_query:
    upcoming_shows.append({
   
      "venue_id" : shows.id,
      "venue_name" : shows.name,
      "venue_image_link" : shows.image_link,
      "start_time" : Show.start_time
    })
 
  return render_template('pages/show_artist.html', artist=artist, upcoming_shows=upcoming_shows,past_shows=past_shows)

  # return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm(request.form)
  artist = Artist.query.get(artist_id)


  artist = {
    "id" : artist.id, 
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website_link": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description":artist.seeking_description,
    "image_link":artist.image_link 
   }
  # TODO: populate form with fields from artist with ID <artist_id>

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  form = ArtistForm(request.form)
  error = False
  artist = Artist.query.get(artist_id)

  try:

      artist.name=form.name.data,
      artist.city=form.city.data,
      artist.state=form.state.data,
      artist.phone=form.phone.data,
      artist.genres=form.genres.data,
      artist.facebook_link=form.facebook_link.data,
      artist.image_link=form.image_link.data,
      artist.website_link=form.website_link.data,
      artist.seeking_venue=form.seeking_venue.data,
      artist.seeking_description=form.seeking_description.data
    

      db.session.add(artist)
      db.session.commit()

  except:  
      error = True
      db.session.rollback()
      print(sys.exc_info())

  finally:
      db.session.close()  

  if error: 
    flash('An error occurred. Venue ' + request.form['name'] + ' could not update .')
    print(sys.exc_info())
 
   # return render_template('forms/edit_artist.html', form=form)
  else:
    flash('Venue ' + request.form['name'] + ' successfully updated!')  

    print(sys.exc_info())


  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)


  venue = {
    "id": venue.id, 
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website_link": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link":venue.image_link 
  }
  # TODO: populate form with values from venue with ID <venue_id>


  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  form = VenueForm(request.form)
  error = False
  venue = Venue.query.get(venue_id)

  try:
      venue.name=form.name.data,
      venue.city=form.city.data,
      venue.state=form.state.data,
      venue.address = form.address.data,
      venue.phone=form.phone.data,
      venue.genres=form.genres.data,
      venue.facebook_link=form.facebook_link.data,
      venue.image_link=form.image_link.data,
      venue.website_link=form.website_link.data,
      venue.seeking_talent=form.seeking_talent.data,
      venue.seeking_description=form.seeking_description.data
      db.session.add(venue)
      db.session.commit()

  except:  
      error = True
      db.session.rollback()
      print(sys.exc_info())

  finally:
      db.session.close()  

  if error: 
    flash('An error occurred. Venue ' + request.form['name'] + ' could not edit please try again.')
    print(sys.exc_info())
 
   # return render_template('forms/edit_venue.html', form=form)
  else:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')  

    print(sys.exc_info())


  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  form = ArtistForm(request.form)
  error = False
  try:
      artist = Artist(

         name=form.name.data,
         city=form.city.data,
         state=form.state.data,
         phone=form.phone.data,
         genres=form.genres.data,
         facebook_link=form.facebook_link.data,
         image_link=form.image_link.data,
         website_link=form.website_link.data,
         seeking_venue=form.seeking_venue.data,
         seeking_description=form.seeking_description.data
      )

      db.session.add(artist)
      db.session.commit()

  except:
      db.session.rollback()
      error = True
      print(sys.exc_info())

  finally:
      print(sys.exc_info())
      db.session.close()
# TODO: on unsuccessful db insert, flash an error instead.
  if error:    
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    print(sys.exc_info())
 
    return render_template('forms/new_artist.html', form=form)
  # on successful db insert, flash success
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
        
  return  redirect(url_for('index'))
 # TODO: modify data to be the data object returned from db insertion

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  data = []
  for show in shows:
    show = ({
        "venue_id" : show.venue_id,
        "venue_name" : db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0], 
        "artist_id" : show.artist_id,
        "artist_name" : db.session.query(Artist.name).filter_by(id=show.artist_id).first()[0], 
        "artist_image_link" : db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0], 
        "start_time" : str(show.start_time)

    })
    data.append(show)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  error = False
  try: 
      show = Show(
          venue_id=form.venue_id.data,
          artist_id=form.artist_id.data,
          start_time=form.start_time.data
        )
       
      db.session.add(show)
      db.session.commit()
      
  except: 
          error = True
          db.session.rollback()
          print(sys.exc_info())
  
  finally:
      print(sys.exc_info())
      db.session.close()  
  
  if error:
      flash('An error occurred please try again')
      print(sys.exc_info())
      return render_template('forms/new_show.html', form=form)
      
  
  else:
         flash('Show was successfully listed!') 
    
  return  redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

