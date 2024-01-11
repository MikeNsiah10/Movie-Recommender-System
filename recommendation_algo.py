from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from model import MovieRating, Movie
import pandas as pd

def get_recommendations(user_id, num_recommendations=10):
    # Load ratings from the database
    ratings = MovieRating.query.all()

    # Convert ratings to DataFrame
    ratings_df = pd.DataFrame([(rating.user_id, rating.movie_id, rating.rating) for rating in ratings],
                              columns=['user_id', 'movie_id', 'rating'])

    # Load all movies from the database
    movies = Movie.query.all()
    movies_df = pd.DataFrame([(movie.id, movie.title) for movie in movies],
                             columns=['movie_id', 'title'])

    # Merge ratings_df with movies_df to get movie titles
    ratings_df = pd.merge(ratings_df, movies_df, on='movie_id')

    # Create a Surprise Dataset using load_from_df
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings_df[['user_id', 'movie_id', 'rating']], reader)

    # Train the model using the full dataset 
    trainset = data.build_full_trainset()
    
    # Configure the model with item-based collaborative filtering
    sim_options = {
        'name': 'cosine',
        'user_based': False  
    }

    # Train the model
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset)

    # Make predictions for the specified user
    user_movies = ratings_df[ratings_df['user_id'] == user_id]['movie_id'].unique()
    movies_to_predict = ratings_df[~ratings_df['movie_id'].isin(user_movies)]['movie_id'].unique()

    predictions = [model.predict(user_id, movie_id) for movie_id in movies_to_predict]

    # Get the top N recommendations based on predicted ratings
    top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:num_recommendations]

    recommended_movies = [{
        'title': movies_df[movies_df['movie_id'] == prediction.iid]['title'].iloc[0],
        'rating': "{:.1f}".format(prediction.est)
    } for prediction in top_n]

    return recommended_movies

