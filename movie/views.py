from django.shortcuts import render
from django.http import HttpResponse

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

# Create your views here.

def home(request):
    # return HttpResponse('<h1>Welcome to home page</h1>')
    # return render(request, 'home.html')
    # return render(request, 'home.html', {'name':'Santiago Manco'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})

def about(request):
    # return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')

    # Obtener todas las peliculas
    all_movies = Movie.objects.all()

    # Crear un diccionario para almacenar la cantidad de peliculas por año
    # y un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_year = {}
    movie_counts_by_genre = {}

    # Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movieGenres = movie.genre.split(", ")
        firstGenre = movieGenres[0] if movieGenres[0] else "None"

        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

        if firstGenre in movie_counts_by_genre:
            movie_counts_by_genre[firstGenre] += 1
        else:
            movie_counts_by_genre[firstGenre] = 1

    # Ancho de las barras
    bar_width = 0.5

    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    
    # --

    # Posiciones de las barras
    bar_positions = range(len(movie_counts_by_genre))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic1 = base64.b64encode(image_png)
    graphic1 = graphic1.decode('utf-8')

    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic, 'graphic1': graphic1})