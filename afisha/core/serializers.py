from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate_name(self, name):
        try:
            Director.objects.get(name=name)
        except Director.DoesNotExist:
            raise ValidationError('Режииссер с таким именем не существует')
        return name


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    duration = serializers.IntegerField(required=True)
    director_id = serializers.IntegerField(required=True, min_value=1)

    def validate_title(self, title):
        title_exists = Movie.objects.filter(title=title).exists()
        if not title_exists:
            return title
        raise ValidationError('Movie with this title already exists')

    def validate_director_id(self, director_id):
        director_exists = Director.objects.filter(id=director_id).exists()
        if not director_exists:
            raise ValidationError('Director with that id does not exists')
        return director_id


class ReviewValidateSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required=True, min_value=1)
    text = serializers.CharField(min_length=10, required=True)
    stars = serializers.IntegerField(min_value=1, max_value=5, required=True)
    movie_id = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = Review
        fields = 'id author text stars'.split()

    def validate_author_id(self, author_id):
        author_exists = User.objects.filter(id=author_id).exists()
        if author_exists:
            return author_id
        raise ValidationError('Пользователя с таким id не существует')

    def validate_movie_id(self, movie_id):
        movie_exists = Movie.objects.filter(id=movie_id).exists()
        if movie_exists:
            return movie_id
        raise ValidationError('Фильма с таким id не существует')
