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

    
    USER_AFTER_REGISTER_ENDPOINT="home_page"
    USER_AFTER_CONFIRM_ENDPOINT="home_page"
    USER_AFTER_LOGIN_ENDPOINT="home_page"
    USER_AFTER_LOGOUT_ENDPOINT="home_page"
    

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


@app.route('/movies', methods=['GET'])
def display_movies():
    movies = Movie.query.limit(100).all()
    return render_template("display_movies.html", movies=movies)


@app.route('/rate_movies', methods=['POST'])
@login_required  # User must be authenticated
def rate_movies():
    if request.method == 'POST':
        movie_id = int(request.form.get('movie_id'))
        rating = int(request.form.get('rating'))
        user_id = current_user.id

        # Check if the user has already rated the movie
        existing_rating = MovieRating.query.filter_by(movie_id=movie_id, user_id=user_id).first()

        if existing_rating:
            # Update the existing rating
            return f' You have already rated the movie with {rating}.'
            
        else:
            # Create a new rating
            new_rating = MovieRating(movie_id=movie_id, user_id=user_id,rating=rating)
            db.session.add(new_rating)

        db.session.commit()

        # Return a simple response (you can customize this as needed)
        return f'Rating submitted successfully! You rated the movie with {rating}.'

    return render_template("rating.html")  # You can adjust this based on your template structure





# Start development web server
if __name__ == '__main__':
    app.run(port=5000, debug=True)
