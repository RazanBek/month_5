from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status


@api_view(['GET'])
def directors_view(request):
    directors = Director.objects.all()
    serializer = DirectorSelialiser(directors, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def director_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = DirectorSelialiser(director).data
    return Response(data=data)


@api_view(['GET'])
def movies_view(request):
    movies = Movie.objects.all()
    serializer = MovieSelialiser(movies, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def movie_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = MovieSelialiser(movie).data
    return Response(data=data)


@api_view(['GET'])
def reviews_view(request):
    reviews = Review.objects.all()
    serializer = ReviewSelialiser(reviews, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def review_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSelialiser(reviews).data
    return Response(data=data)


@api_view(['GET'])
def film_list_review_view(request):
    movie = Movie.objects.all()
    serializer = FilmListSerializer(movie, many=True)
    return Response(data=serializer.data)
