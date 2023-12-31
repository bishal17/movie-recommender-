import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyZDg5Y2IxZmQ4NjZhNTg4YzYwZmQ1YTk2MjYzNWJhNSIsInN1YiI6IjY1OTAzMjQxNTFhNjRlMDJlMmY0MzA3NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DpMUoXvWkO9xb9ogpeRtUp3-hmOJtMxQThE9gB-zuTw"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path is not None:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            st.warning(f"No poster available for movie {movie_id}")
            return None
    else:
        st.error(f"Error fetching data for movie {movie_id}. Status code: {response.status_code}")
        return None


def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return [], []  # Return empty lists if the movie is not found

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        try:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            poster = fetch_poster(movie_id)
            if poster:
                recommended_movie_posters.append(poster)
                recommended_movie_names.append(movies.iloc[i[0]].title)
        except IndexError:
            # Handle the case where the index is out of bounds
            continue

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')

# Open and load the pickled movie list
with open('movie_list.pkl', 'rb') as file:
    movies = pickle.load(file)

# Open and load the pickled similarity matrix
with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

# Example check for similarity matrix
if similarity is None or len(similarity) != len(movies):
    st.error("Error with the similarity matrix")
    st.stop()

movie_list = movies['title'].values
movie_selected = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(movie_selected)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
