from rest_framework import serializers
from .models import Movie, Director, Review
from django.contrib.auth.models import User


class ReviewMovieSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Review
        fields = 'id author text stars'.split()


class FilmListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    reviews = ReviewMovieSerializer(many=True)

    class Meta:
        model = Movie
        fields = 'id title description duration director reviews rating'.split()

    def get_rating(self, movie):
        return movie.rating()


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id username first_name last_name email'.split()


class DirectorSelialiser(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = '__all__'

    def get_movies_count(self, director):
        return director.movie_count()


class MovieSelialiser(serializers.ModelSerializer):
    director = DirectorSelialiser()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_rating(self, movie):
        return movie.rating()


class MovieNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'title'.split()


class ReviewSelialiser(serializers.ModelSerializer):
    author = UserSimpleSerializer()
    movie = MovieNameSerializer()

    class Meta:
        model = Review
        fields = '__all__'
