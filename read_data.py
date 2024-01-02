import csv
from sqlalchemy.exc import IntegrityError
from model import Movie, User, MovieGenre, MovieLink, MovieTag,MovieRating
from datetime import datetime

def check_and_read_data(db):
    # Check if we have movies in the database
    # Read data if the database is empty
    if (
        Movie.query.count() == 0
        and MovieGenre.query.count() == 0
        and MovieLink.query.count() == 0
        and MovieTag.query.count() == 0
    ):
        # Read movies from csv
        with open('data/movies.csv', newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            count = 0
            for row in reader:
                if count > 0:
                    try:
                        id = row[0]
                        title = row[1]
                        movie = Movie(id=id, title=title)
                        db.session.add(movie)
                        genres = row[2].split('|')  # Genres is a list of genres
                        for genre in genres:
                            # Add each genre to the movie_genre table
                            movie_genre = MovieGenre(movie_id=id, genre=genre)
                            db.session.add(movie_genre)
                        db.session.commit()  # Save data to the database
                    except IntegrityError:
                        print("Ignoring duplicate movie: " + title)
                        db.session.rollback()
                        pass
                count += 1
                if count % 100 == 0:
                    print(count, "movies read")
        with open('data/links.csv', newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            count = 0
            for row in reader:
                if count > 0:
                    try:
                        movie_id = int(row[0])
                        imdb_id = int(row[1])
                        tmdb_id = int(row[2]) if row[2].isdigit() else None
                        movie_link = MovieLink(movie_id=movie_id, imdb_id=imdb_id, tmdb_id=tmdb_id)
                        db.session.add(movie_link)
                        db.session.commit()  # Save data to the database
                    except IntegrityError:
                        print("Ignoring duplicate link for movie_id: " + movie_id)
                        db.session.rollback()
                        pass
                count += 1
                if count % 100 == 0:
                    print(count, "links read")
        with open('data/tags.csv', newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            count = 0
            for row in reader:
                if count > 0:
                    try:
                        user_id = int(row[0])
                        movie_id = int(row[1])
                        tag = row[2]
                        # Convert Unix timestamp to datetime
                        timestamp = datetime.fromtimestamp(int(row[3]))
                        movie_tag = MovieTag(user_id=user_id, movie_id=movie_id, tag=tag, timestamp=timestamp)
                        db.session.add(movie_tag)
                        db.session.commit()  # Save data to the database
                    except IntegrityError:
                        print("Ignoring duplicate tag for movie: " + tag)
                        db.session.rollback()
                        pass
                count += 1
                if count % 100 == 0:
                    print(count, "tags read")
        with open('data/ratings.csv', newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            count = 0
            for row in reader:
                if count > 0:
                    try:
                        user_id = int(row[0])
                        movie_id = int(row[1])
                        rating = float(row[2])
                        timestamp = datetime.fromtimestamp(int(row[3]))
                        print(f"Processing Rating: User_ID={user_id}, Movie_ID={movie_id}, Rating={rating}")

                        # Create user objects for the ratings
                         
                        user = User.query.filter_by(id=user_id).first()
                        if not user:
                        # If user does not exist, create a new user
                           user = User(id=user_id, username=f'user_{user_id}')
                           db.session.add(user)

                        # Create MovieRating object
                        movie_rating = MovieRating(user_id=user_id, movie_id=movie_id, rating=rating, timestamp=timestamp)
                        db.session.add(movie_rating)
                        # Save data to the database
                        db.session.commit()  
                    except IntegrityError as e:
                        print(f"IntegrityError: {e}")
                        db.session.rollback()
                        pass
                count += 1
                if count % 100 == 0:
                    print(count, "ratings read")


