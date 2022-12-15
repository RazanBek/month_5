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
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={"errors": serializer.errors})
        name = serializer.validated_data['name']
        director = serializer.validated_data['director']
        directorr = Director.objects.create(name=name, director=director)
        directorr.save()
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
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
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
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        duration = serializer.validated_data['duration']
        director_id = serializer.validated_data['director_id']
        movie = Movie.objects.create(title=title, description=description, duration=duration, director_id=director_id)
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
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        duration = serializer.validated_data['duration']
        director_id = serializer.validated_data['director_id']
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
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author_id = serializer.validated_data['author_id']
        text = serializer.validated_data['text']
        stars = serializer.validated_data['stars']
        movie_id = serializer.validated_data['movie_id']

        review = Review.objects.create(
            author_id=author_id,
            text=text,
            stars=stars,
            movie_id=movie_id
        )
        review.save()
        return Response(data={"message": "review created successfully", "review": ReviewSelialiser(review).data})


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
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author_id = serializer.validated_data['author_id']
        text = serializer.validated_data['text']
        stars = serializer.validated_data['stars']
        movie_id = serializer.validated_data['movie_id']

        reviews.author_id = author_id
        reviews.text = text
        reviews.stars = stars
        reviews.movie_id = movie_id

        reviews.save()

        return Response(data={"message": "review updated successfully", "review": ReviewSelialiser(reviews).data})


@api_view(['GET'])
def film_list_review_view(request):
    movie = Movie.objects.all()
    serializer = FilmListSerializer(movie, many=True)
    return Response(data=serializer.data)
