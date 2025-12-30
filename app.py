import streamlit as st
import pandas as pd
import pickle
import requests
from dotenv import load_dotenv
import os

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

retry_strategy = Retry(
    total=5,
    backoff_factor=0.6,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)


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


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    api_key = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

    response = session.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    poster_path = data["poster_path"]

    return f"https://image.tmdb.org/t/p/w500{poster_path}"


# Initialize session state
if 'current_overview' not in st.session_state:
    st.session_state.current_overview = None
if 'current_overview_title' not in st.session_state:
    st.session_state.current_overview_title = None


st.markdown("""
    <style>
            
    html, body {
        margin: 0;
        padding: 0;
        height: 100%;
    }

    .stApp {
        margin-top: 0;
        padding-top: 0;
    }


    header[data-testid="stHeader"] {
        display: none;
    }

    section[data-testid="stMain"] {
        padding-top: 0;
    }

    
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
    
    poster_urls = {}

    for _, row in recommendations.iterrows():
        poster_urls[row["movie_id"]] = fetch_poster(row["movie_id"])

    # Show movie grid
    for i in range(0, 10, 5):  
        cols = st.columns(5)  
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie = recommendations.iloc[j]
                with col:
                    st.image(poster_urls[movie["movie_id"]], width=130)
                    st.write(movie['title'])
                    if st.button(f"Overview", key=f"btn_{j}"):
                        st.session_state.current_overview = movie['overview']
                        st.session_state.current_overview_title = movie['title']
    
    # Show overview if selected
    if st.session_state.current_overview:
        with overview_placeholder.container():
            st.subheader(f"Movie Overview — {st.session_state.current_overview_title}")
            st.write(st.session_state.current_overview)
            if st.button("Close Overview", key="close_overview"):
                st.session_state.current_overview = None
                st.session_state.current_overview_title = None
                st.rerun()


