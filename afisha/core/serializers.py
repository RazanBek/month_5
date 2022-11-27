from rest_framework import serializers
from .models import Movie, Director, Review


class DirectorSelialiser(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieSelialiser(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewSelialiser(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
