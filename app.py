import streamlit as st
import pickle
import pandas as pd
import requests
import base64

st.set_page_config(page_title ="Movie Recommendation System",
                       page_icon='🎬',
                       layout='wide')

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer:after{
            content:'© Sanyam Sharma';
            display:block;
            position:relative;
            color:rgba(250, 250, 250, 0.4);
            padding:5px;
            top=3px;
            }
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def set_bg_hack(main_bg):
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


set_bg_hack('background.png')

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = pd.Series(movies.title.values)
#similarity = pickle.load(open('similarity.pkl', 'rb'))
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 5000, stop_words = 'english')
vectors = cv.fit_transform(movies_tag['tag']).toarray()
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(vectors)

def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=46021bb9e6da9b0b2e5a50dc4196528f'.format(movie_id))
    json_data = response.json()
    return "https://image.tmdb.org/t/p/w500"+json_data['poster_path']


def recommend(movie):
    index = movies_list[movies_list == movie].index.values[0]
    top5_movies = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    movies_posters = []
    for index, distance in top5_movies:
        recommended_movies.append(movies_list[index])
        movies_posters.append(get_poster(movies.id[index]))

    return recommended_movies, movies_posters


st.title("Movie Recommendation System")

movie_name = st.selectbox("Enter the Movie Name:",movies_list)

if st.button("Recommend"):
    with st.spinner('Finding Recommendations...'):
        st.subheader("Your Recommendations are:")
        recommendations, posters = recommend(movie_name)
        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.subheader(recommendations[i])

