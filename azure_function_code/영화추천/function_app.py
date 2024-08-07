import logging
import pandas as pd
import numpy as np
import azure.functions as func
import random
import json

# 감정을 장르로 매핑하는 함수
def emotion_genre_mapping(emotion):
    emotion_genre_mapping = {
        'positive': ['Action', 'Adventure', 'Science Fiction', 'Fantasy', 'Animation', 'Family', 'Comedy', 'Romance', 'Music', 'Documentary', 'TVMovie'],
        'negative': ['Animation', 'Family', 'Comedy', 'Music', 'TVMovie']
    }
    return emotion_genre_mapping.get(emotion, [])

# type 1 인 경우 인기도 / 평점 기반 추천
def recommend_type1(movies, num_recommendations=10):
    top_movies = movies.sort_values(by=['popularity', 'vote_average'], ascending=False).head(50)
    recommended_movies = top_movies.sample(n=num_recommendations, replace=False)
    titles = recommended_movies['title'].tolist()
    homepages = recommended_movies['homepage'].tolist()
    return titles, homepages

# 유사도 기반 영화 추천
def recommend_by_similarity(movie_index, cosine_sim_adj, movies, num_recommendations=10):
    sim_scores = list(enumerate(cosine_sim_adj[movie_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = movies.iloc[movie_indices]
    titles = recommended_movies['title'].tolist()
    homepages = recommended_movies['homepage'].tolist()
    return titles, homepages

# 감정과 장르를 기반으로 유사도 추천 함수
def recommend_by_emotion_and_similarity(emotion, movies, cosine_sim_adj, num_recommendations=10):
    genres = emotion_genre_mapping(emotion)
    if not genres:
        return [], []

    genre_filtered_movies = movies[movies['genres'].apply(lambda x: any(genre in x for genre in genres))]
    
    if genre_filtered_movies.empty:
        return [], []

    random_movie_index = random.choice(genre_filtered_movies.index)
    return recommend_by_similarity(random_movie_index, cosine_sim_adj, genre_filtered_movies, num_recommendations)

movies = pd.read_csv("processed_movies.csv")
cosine_sim_adj = np.load("cosine_sim_adj.npy")

app = func.FunctionApp()

@app.route(route="RecommendMovies", auth_level=func.AuthLevel.FUNCTION)
def recommend_movies(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    preferred_type = req.params.get('type')
    if not preferred_type:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            preferred_type = req_body.get('type')

    if preferred_type == '1':
        titles, homepages = recommend_type1(movies)
    elif preferred_type == '2':
        input_emotion = req.params.get('emotion')
        if not input_emotion:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                input_emotion = req_body.get('emotion')
        if not input_emotion:
            return func.HttpResponse(
                "Please pass an emotion on the query string or in the request body",
                status_code=400
            )
        titles, homepages = recommend_by_emotion_and_similarity(input_emotion, movies, cosine_sim_adj)
    else:
        return func.HttpResponse(
            "Please pass a valid type (1 or 2) on the query string or in the request body",
            status_code=400
        )

    response_data = {
        "titles": titles,
        "homepages": homepages
    }

    return func.HttpResponse(json.dumps(response_data), mimetype="application/json")
