# Contains parts from: https://flask-user.readthedocs.io/en/latest/quickstart_app.html
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_user import login_required, current_user,UserManager
from flask import Flask
from recommendation_algo import get_recommendations

from model import db, User, Movie,MovieLink,MovieTag,MovieGenre,MovieRating
from read_data import check_and_read_data

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movie_recommender_app.sqlite'  # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "Movie Recommender"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = True  # Simplify register form
    

# Create Flask app
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')  # configuration
app.app_context().push()  # create an app context before initializing db
db.init_app(app)  # initialize database
db.create_all() # create database if necessary
user_manager = UserManager(app, db, User)  # initialize Flask-User management


@app.cli.command('initdb')
def initdb_command():
    global db
    """Creates the database tables."""
    check_and_read_data(db)
    print('Initialized the database.')

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    # render home.html template
    return render_template("home.html")

@app.route('/recommendations')
@login_required
def recommendations():
    # Get recommendations for the current user
    recommended_movie_titles = get_recommendations(current_user.id)

    return render_template('recommendations.html', recommended_movie_titles=recommended_movie_titles)


@app.route('/movies', methods=['GET', 'POST'])
@login_required  # User must be authenticated
def rate_movies():
    # String-based templates
    #retrieve 100 movies from the database for testing
    movies = Movie.query.limit(100).all()

    if request.method == 'POST':
        # Handle movie rating submission
        movie_id = int(request.form.get('movie_id'))
        rating = float(request.form.get('rating'))

        # Check if the user has already rated the movie
        already_rated = MovieRating.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()

        if already_rated:
            flash('You have already rated this movie', 'warning')
        else:
            # Create a new MovieRating entry
            new_rating = MovieRating(user_id=current_user.id, movie_id=movie_id, rating=rating)
            db.session.add(new_rating)
            db.session.commit()

            flash('Rating submitted successfully', 'success')

    return render_template("rate_movies.html", movies=movies)




# Start development web server
if __name__ == '__main__':
    app.run(port=5000, debug=True)
