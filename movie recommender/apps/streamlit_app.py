import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# -----------------------------
# STEP 1: Load and Prepare Data
# -----------------------------

@st.cache_data
def load_data():
    # Load ratings data (not used directly in this app)
    ratings = pd.read_csv("data/u.data", sep='\t', names=['userId', 'movieId', 'rating', 'timestamp'])

    # Load movie metadata with genres
    movie_cols = ['movieId', 'title', 'release_date', 'video_release', 'IMDb_URL'] + [f'genre_{i}' for i in range(19)]
    movies = pd.read_csv("data/u.item", sep='|', names=movie_cols, encoding='latin-1')

    # Combine genre columns into a single string (e.g., 'Action Comedy')
    genre_columns = movie_cols[5:]
    movies['genres'] = movies[genre_columns].apply(
        lambda row: ' '.join([genre_columns[i] for i, val in enumerate(row) if val == 1]),
        axis=1
    )

    # Keep only required columns
    movies = movies[['movieId', 'title', 'genres']]
    return movies

# Load the movies dataset
movies = load_data()

# ---------------------------------
# STEP 2: Build the TF-IDF Model
# ---------------------------------

# Convert genres to TF-IDF vectors
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])

# Compute cosine similarity matrix between all movies
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create a lookup Series to map titles to DataFrame indices
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# ---------------------------------
# STEP 3: Define Recommendation Logic
# ---------------------------------

def recommend(title, num_recommendations=5):
    # Check if the movie exists in our index
    if title not in indices:
        return pd.DataFrame(columns=['title', 'genres'])

    idx = indices[title]

    # Get similarity scores for all movies with the selected one
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort by similarity score (excluding itself)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top recommended movies
    return movies.iloc[movie_indices][['title', 'genres']]

# ---------------------------------
# STEP 4: Streamlit App Interface
# ---------------------------------

st.set_page_config(page_title="🎬 Movie Recommender")
st.title("🎬 Movie Recommendation System")
st.markdown("Get recommendations based on movie genres using **Content-Based Filtering (TF-IDF)**.")

# Dropdown to select a movie
movie_list = movies['title'].sort_values().tolist()
selected_movie = st.selectbox("Choose a movie you like:", movie_list)

# Button to generate recommendations
if st.button("Recommend"):
    st.subheader(f"Because you liked *{selected_movie}*...")
    recommendations = recommend(selected_movie)

    if recommendations.empty:
        st.warning("Sorry! No recommendations found.")
    else:
        for _, row in recommendations.iterrows():
            st.markdown(f"**🎞 {row['title']}**  \nGenres: *{row['genres']}*")

st.markdown("---")
st.caption("Made with 🧠 using MovieLens 100k | Content-Based Filtering")
