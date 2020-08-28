from django.shortcuts import render, redirect
import pandas as pd 
from .naver_genre_recommend import create_data ,create_tfidf_matrix , create_count_matrix, calculate_similarity ,find_similar_movies
# Create your views here.

def home(request):

    if request.method == "POST":

        input_movie = request.POST["movie_sh"]

        return redirect("result", input_movie)

    return render(request,'home.html')

def result(request, input_movie):

    movie = create_data()
    t_matrix = create_tfidf_matrix(movie)
    t_similarity = calculate_similarity(t_matrix)
    t_result = find_similar_movies(movie, t_similarity, input_movie)
    
    c_matrix = create_count_matrix(movie)
    c_similarity = calculate_similarity(c_matrix)
    c_result = find_similar_movies(movie, c_similarity, input_movie)

    context = {
        't_result' : t_result,
        'c_result' : c_result,
        'input_movie' : input_movie
    }

    return render(request, 'result.html', context)