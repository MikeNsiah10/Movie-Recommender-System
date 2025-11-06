## Movie Recommender System

# Project Overview

This repository is a movie recommender system built or created using the movielens datasets , a KNNBasic Model from scikit-surprise,FLask and sql database.


## Repository Structure
```
/data                              # Contains MovieLens dataset
/instance                          #initialise and populate the database
/static                         
    ├── styles.css                 # stylesheet to apply style to our templates
/templates
    ├── display_movies.html        # html template to movie display
    ├── flask_user.html            # html template for user login or logout
    └── home.html                  # homepage
    ├──index.html                  # html template for how the recommender works
    ├── rating.html                # display message when one rates a movie
    ├── recoomendations.html       # list of recommended movies
/model.py                          # The user data model(db model)
/read_data.py                      # script to read data from the movie lens csv files
/recommendation_algo.py            # KNNBasic algorithm to predicting recommendations for the users
/recommender.py                    # the main flask app
/requirements.txt                  # list of dependencies
```
## Requirements

To use this repository, follow these steps:

1. Clone the Repository:
   ```
      git clone https://github.com/MikeNsiah10/Movie-Recommender-System.git
   cd Movie-Recommender-System
   ```

2. Setting Up a Python Environment
It is recommended to use a virtual environment to manage the dependencies for this project. A virtual environment helps to isolate your project's dependencies from your global Python environment, avoiding potential conflicts.
```
   # Create a virtual environment in a directory named 'env'
   python3 -m venv env

    # Activate the virtual environment
    # On Windows
    env\Scripts\activate
    # On macOS/Linux
    source env/bin/activate
```
   
3. Install Dependencies:
   Make sure you have the necessary libraries installed. You can use pip to install them:
   ```
       pip install -r requirements.txt
   ```
   

4. Run the app
    ```
   flask --app recommender.py run or  flask --app recommender.py run --debug for debugging
    ```
   
