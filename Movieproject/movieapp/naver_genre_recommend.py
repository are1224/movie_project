# -*- coding: utf-8 -*-
"""Naver_Genre_recommend.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MJiq_2ilAuahZmWd0iVfNEuEOOnhZhsY
"""
import csv
import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def create_data():
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 1000)

    movies = pd.read_csv('./movies_naver.csv')
    movies = movies.loc[:, ['title', 'genres']]

    # 문자열 -> 딕셔너리 형태로 변환
    movies['genres'] = movies['genres'].apply(literal_eval)


    # i = 0
    # for row in movies['genres']:
    #     genres = []
    #     for ele in row:
    #         genres.append(ele['name'])
    #     movies['genres'][i] = genres
    #     i = i + 1

    # 딕셔너리 형태를 깔끔하게 장르에 해당하는 부분만 뽑아서 문자열화
    # [{}, {}, {}, {}] -> [장르, 장르, 장르, 장르]
    movies['genres'] = movies['genres'].apply(lambda x : [y['name'] for y in x])

    # [장르, 장르, 장르, 장르] -> 장르 장르 장르 장르
    movies['genres'] = movies['genres'].apply(lambda x : ' '.join(x))
    # print(movies['genres'])
    return movies

"""# TFIDF"""

def create_tfidf_matrix(movies):
    # ngram_range=(1, 2) 는 단어를 1개 혹은 2개 연속으로 보겠다
    tfidf_vec = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_matrix = tfidf_vec.fit_transform(movies['genres'])
    # print(tfidf_vec.vocabulary_.items())
    # 4803은 영화의 개수, 276은 단어의 개수 -> 하나의 영화를 276개 열을 가진 벡터로 표현
    
    return tfidf_matrix

    # action adventure fantasy
    # adventure fantasy
    # adventure
    # fantasy

"""# Count (빈도수)"""

def create_count_matrix(movies):
    count_vec = CountVectorizer(ngram_range=(1, 2))
    count_matrix = count_vec.fit_transform(movies['genres'])
    return count_matrix   

def calculate_similarity(matrix):
    # 유사도 행렬 (4803, 4803)
    # 1, 1 (1번째 영화와 1번재 영화의 유사도)
    # 1, 1 / 1, 2 / .... / 1, 4803 -> 1번째 영화와 1~4803번재 영화의 유사도
    # 2, 1 / 2, 2 / .... / 2, 4803 -> 2번째 영화와 1~4803번째 영화의 유사도
    # ....
    # 4803, 1 / 4803, 2 / .... / 4803, 4803 -> 4803번째 영화와 1~4803번째 영화의 유사도


    # 4803개의 영화랑 4803개의 영화끼리 유사도를 구하겠다!
    # 자신과의 유사도는 1
    genres_similarity = cosine_similarity(matrix, matrix)
    # 유사도 값이 높은 영화의 제목
    # 유사도 값이 높은 순으로 인덱스 값을 뽑아낸다
    similar_index = np.argsort(-genres_similarity)
    return similar_index


def find_similar_movies(movies, similar_index, input_movie):
    # 사용자가 입력한 영화의 인덱스 값을 찾아내고
    # similar_index 에 기록된 유사한 영화 인덱스를 찾아내고
    # 유사한 영화 인덱스를 토대로 영화 이름을 찾아내면 된다!

    movie_index = movies[movies['title']==input_movie].index.values
    similar_movies = similar_index[movie_index, 1:6]
    # 인덱스로 사용하기 위해서는 1차원으로 변형해줘야하기 때문
    similar_movies_index = similar_movies.reshape(-1)

    return movies.iloc[similar_movies_index]['title']

############시범용 