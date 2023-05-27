import streamlit as st
import pickle
import pandas as pd
import requests

# Load movie data and cosine similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
cosine_sim = pickle.load(open('similarity.pkl', 'rb'))

# Fetch movie poster from API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=144806e8cb6668e2b57bba0635d7a401&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Generate movie recommendations
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    cosine_similarities = cosine_sim[index]
    similar_movies_indices = sorted(list(enumerate(cosine_similarities)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in similar_movies_indices:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Formatting the webpage
st.title('Movie Recommendation System')
st.subheader('Developed by Hrithik Shukla :sunglasses:')
selected_movie_name = st.selectbox('Enter your choice of movie', movies['title'].values)

with st.expander("View our recommendations"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    for i in range(5):
        st.write(recommended_movie_names[i])
        st.image(recommended_movie_posters[i])