# Movie Recommendation System

This project is a **content-based movie recommendation system** built using **machine learning** and a sleek **Streamlit** interface. Users can select a movie and receive 10 similar movie recommendations along with their posters and overviews powered by the TMDB API.

---

## Project Structure

```bash
movie_pro/
│
├── app.py                  # Streamlit app frontend
├── MovieRec.ipynb          # Jupyter Notebook for feature extraction and similarity matrix generation
├── movies.csv              # Movie metadata (title, ID, etc.)
├── credits.csv             # Cast and crew details
├── movie_data.pkl          # Pickled data: movies DataFrame and cosine similarity matrix (not pushed to GitHub)
├── .env                    # Environment file to store your TMDB API key (not pushed to GitHub)
├── .gitignore              # Git ignored files like .env and .pkl
└── README.md               # Project documentation
```

---

## How It Works

- The notebook (`MovieRec.ipynb`) combines data from `movies.csv` and `credits.csv`.
- Features are extracted using:
  - Cast, crew, genres, keywords
  - TF-IDF or CountVectorizer for vector representation
- A **cosine similarity matrix** is computed and saved as `movie_data.pkl`.
- The `app.py` loads this data and displays:
  -  Movie posters using TMDB API
  -  Overviews with a sleek UI
  -  Real-time recommendations with 10 similar movies

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/srinithi0406/Movie_Recommendation_ml.git
cd Movie_Recommendation_ml
```

### 2. Create a `.env` File for TMDB API Key

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

### 3. Install Required Packages

```bash
pip install numpy pandas streamlit requests python-dotenv scikit-learn
```
### 4. Run the Streamlit App

```bash
streamlit run app.py
```

---

## Note on `movie_data.pkl`
Regenerate it by running the `MovieRec.ipynb` notebook **locally**.
