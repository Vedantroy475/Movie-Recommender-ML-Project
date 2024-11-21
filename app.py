import pickle
import streamlit as st
import requests
import os
import gdown

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None

# Recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Streamlit app
st.set_page_config(page_title="Movie Recommender System", layout="wide")

# Add title and introduction
st.title("🎥 Movie Recommender System Machine Learning Project")
st.markdown("""
<style>
     body {
        background-color: #adcff0;
    }
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        padding-bottom: 20px;
    }
    .watermark {
        position: fixed;
        bottom: 0px;
        left: 0px;
        width: 100%;
        text-align: center;
        font-size: 14px;
        color: white;
        background-color: #2c3e50; /* Dark blue-gray background for the footer */
        padding: 10px 0;
        border-top: 3px solid #1abc9c;
    }
</style>
""", unsafe_allow_html=True)

# App description
st.markdown(
    "<p class='main-header'>Welcome to the Movie Recommender System! Find personalized movie recommendations just for you.</p>",
    unsafe_allow_html=True
)

# Google Drive URLs for the pickle files
movie_list_url = "https://drive.google.com/uc?id=1QRwSbKMMprtvmhDBitVKtX4XETKcULTz"
similarity_url = "https://drive.google.com/uc?id=1OuiCbt31Zv99y9lLPDkOK2rBjhT1YXks"

# File names
movie_list_file = "movie_list.pkl"
similarity_file = "similarity.pkl"

# Function to download a file from Google Drive
def download_file(url, output):
    if not os.path.exists(output):
        with st.spinner(f"Downloading {output}..."):
            gdown.download(url, output, quiet=False)
    else:
        print(f"{output} already exists, skipping download.")

# Download the pickle files
download_file(movie_list_url, movie_list_file)
download_file(similarity_url, similarity_file)

# Load data
try:
    movies = pickle.load(open(movie_list_file, 'rb'))
    similarity = pickle.load(open(similarity_file, 'rb'))
except Exception as e:
    st.error(f"Error loading pickle files: {e}")
    st.stop()

# Dropdown to select a movie
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown:", movie_list)

# Display recommendations
if st.button('🎬 Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.markdown("### Recommended Movies for You:")
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[i], width=150, caption=recommended_movie_names[i])

# Add watermark
st.markdown("""
<div class='watermark'>
    Made by <strong>Vedant Roy</strong> | Email: vedantroy3@gmail.com | 
    <a href="https://github.com/Vedantroy475" target="_blank">My GitHub Profile</a>|<a href="https://www.linkedin.com/in/vedant-roy-b58117227/" target="_blank">My Linkedin Profile</a>
</div>
""", unsafe_allow_html=True)
