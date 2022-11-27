from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status


@api_view(['GET', 'POST'])
def directors_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSelialiser(directors, many=True)
        return Response(data=serializer.data)
    else:
        name = request.data.get('name', 'Ваня')
        director = Director.objects.create(name=name)
        director.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={
                            'message': 'director created successfully',
                            'directors': DirectorSelialiser(director).data
                        })


@api_view(['GET', 'PUT', 'DELETE'])
def director_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorSelialiser(director).data
        return Response(data=data)
    elif request.method == "DELETE":
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        name = request.data.get('name', 'Ваня')
        director.name = name
        director.save()
        return Response(
            data={
                'message': 'director created successfully',
                'directors': DirectorSelialiser(director).data
            })


@api_view(['GET', 'POST'])
def movies_view(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSelialiser(movies, many=True)
        return Response(data=serializer.data)
    else:
        title = request.data.get("title", "")
        description = request.data.get("description", "")
        duration = request.data.get("duration", 0)
        director = request.data.get("director_id", 1)
        movie = Movie.objects.create(title=title, description=description,
                                     duration=duration, director_id=director)
        movie.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={"message": "movie created successfully", "movie": MovieSelialiser(movie).data})


@api_view(['GET', 'PUT', 'DELETE'])
def movie_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSelialiser(movie).data
        return Response(data=data)
    elif request.method == 'PUT':
        title = request.data.get("title", movie.title)
        description = request.data.get("description", movie.description)
        duration = request.data.get("duration", movie.duration)
        director_id = request.data.get("director_id", movie.director_id)
        movie.title = title
        movie.description = description
        movie.duration = duration
        movie.director_id = director_id
        movie.save()
        return Response(data={"message": "movie updated successfully",
                              "movie": MovieSelialiser(movie).data})
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data={"message": "movie deleted successfully"})


@api_view(['GET', 'POST'])
def reviews_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSelialiser(reviews, many=True)
        return Response(data=serializer.data)
    else:
        author = request.data.get("author", None)
        text = request.data.get("text", " ")
        movie = request.data.get("movie", None)
        stars = request.data.get("stars", 1)
        review = Movie.objects.create(author=author, text=text,
                                      movie=movie, stars=stars)
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={"message": "review created successfully",
                              "review": ReviewSelialiser(movie).data})


@api_view(['GET', 'PUT', 'DELETE'])
def review_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        data = ReviewSelialiser(reviews).data
        return Response(data=data)

    elif request.method == 'DELETE':
        reviews.delete()
        return Response(data={"message": "review deleted successfully"})

    elif request.method == 'PUT':
        author_id = request.data.get("author_id", reviews.author_id)
        text = request.data.get("text", reviews.text)
        stars = request.data.get("stars", reviews.stars)
        movie_id = request.data.get("movie_id", reviews.movie_id)

        reviews.author_id = author_id
        reviews.text = text
        reviews.stars = stars
        reviews.movie_id = movie_id
        reviews.save()
        return Response(data={"message": "review updated successfully",
                              "review": ReviewSelialiser(reviews).data})


@api_view(['GET'])
def film_list_review_view(request):
    movie = Movie.objects.all()
    serializer = FilmListSerializer(movie, many=True)
    return Response(data=serializer.data)
