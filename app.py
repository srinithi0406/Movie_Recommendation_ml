import streamlit as st
import pandas as pd
import pickle
import requests
from dotenv import load_dotenv
import os

load_dotenv()

with open('movie_data.pkl', 'rb') as fh:
    movies, cosine =pickle.load(fh)

def get_recommendation(title, cosine=cosine):
  idx=movies[movies['title']==title].index[0]
  sim_scores=list(enumerate(cosine[idx]))
  sim_scores=sorted(sim_scores, key=lambda x:x[1], reverse=True)
  sim_scores=sim_scores[1:11]
  movie_idx= [i[0] for i in sim_scores]
  return movies[['title', 'movie_id', 'overview']].iloc[movie_idx]

def fetch_poster(movie_id):
    api_key = os.getenv("TMDB_API_KEY")
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path

# Initialize session state
if 'current_overview' not in st.session_state:
    st.session_state.current_overview = None

st.markdown("""
    <style>
    
    .stApp {
        background-image: linear-gradient(135deg, #0d1b2a, #1b263b, #415a77, #1e2746);
        background-size: cover;
        color: white;
    }

    html, body, [class*="css"] {
        color: white;
        background-color: transparent;
    }

    .stSelectbox label {
        color: white !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1b263b !important;
        color: white !important;
    }

    .stButton>button {
    color: white !important;
    background-color: #1b263b !important;
    border: 2px solid #ffffff !important;  /* White border */
    padding: 0.5em 1em;
    border-radius: 8px;
    font-weight: 600;
    transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #415a77 !important;
        border-color: #00C2FF !important;  /* Light blue border on hover */
        color: #ffffff !important;
    }

    </style>
""", unsafe_allow_html=True)

st.title('The Ultimate Movie Recommedation site')
select_movie=st.selectbox("Select a movie to get recommendtations:", movies['title']. values)
select_movie_row=movies[movies['title']==select_movie]

if not select_movie_row.empty:
    selected_movie_id = select_movie_row.iloc[0]['movie_id']
    poster_url = fetch_poster(selected_movie_id)
    st.sidebar.image(poster_url, caption=select_movie, use_container_width=True)

if st.button('Recommend'):
    recommendations = get_recommendation(select_movie)
    st.session_state.recommendations = recommendations
    st.session_state.current_overview = None  

if 'recommendations' in st.session_state:
    recommendations = st.session_state.recommendations
    overview_placeholder = st.empty()
    
    # Show movie grid
    for i in range(0, 10, 5):  
        cols = st.columns(5)  
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie = recommendations.iloc[j]
                with col:
                    st.image(fetch_poster(movie['movie_id']), width=130)
                    st.write(movie['title'])
                    if st.button(f"Overview", key=f"btn_{j}"):
                        st.session_state.current_overview = movie['overview']
    
    # Show overview if selected
    if st.session_state.current_overview:
        with overview_placeholder.container():
            st.subheader("Movie Overview")
            st.write(st.session_state.current_overview)
            if st.button("Close Overview", key="close_overview"):
                st.session_state.current_overview = None
                st.rerun()


