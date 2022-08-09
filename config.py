import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://jvoppuakifcjlm:fc1ba1a0767f76e61c37983b5418a0498e9d4cdf9a39a854c59c4eef5b57ba40@ec2-34-234-240-121.compute-1.amazonaws.com:5432/dd7ecs14pelnip'
SQLALCHEMY_TRACK_MODIFICATIONS = True
