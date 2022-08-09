import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://pecpzrkqpbhsqx:9054a03e51f8165db3f11b3a12e9000152a6ebff5aab5310eea58a51b4b2c9d5@ec2-34-235-31-124.compute-1.amazonaws.com:5432/d5oshmfjeiol0s'
SQLALCHEMY_TRACK_MODIFICATIONS = True
