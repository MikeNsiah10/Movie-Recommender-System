from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

db = SQLAlchemy()

# Define the User data-model.
# NB: Make sure to add flask_user UserMixin as this adds additional fields and properties required by Flask-User
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    ratings=db.relationship('MovieRating',backref='user')

# Movie data table
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    genres = db.relationship('MovieGenre', backref='movie', lazy=True)
    links = db.relationship('MovieLink', back_populates='movie', lazy=True)
    tags = db.relationship('MovieTag', back_populates='movie', lazy=True)

# MovieGenre data table
class MovieGenre(db.Model):
    __tablename__ = 'movie_genres'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    genre = db.Column(db.String(255), nullable=False, server_default='')

# MovieLink data table
class MovieLink(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.Integer)
    tmdb_id=db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    movie = db.relationship("Movie", back_populates="links")

# movietag data table
class MovieTag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tag = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    movie = db.relationship("Movie", back_populates="tags")

#MovieRating data table
class MovieRating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 
    rating = db.Column(db.Float, nullable=False)


