from django.db import models
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(default='Ваня', max_length=65)

    def __str__(self):
        return self.name

    def movie_count(self):
        return len(self.movies.all())


class Movie(models.Model):
    title = models.CharField(null=True, max_length=60)
    description = models.TextField(null=True)
    duration = models.IntegerField(null=True)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True, related_name='movies')

    def __str__(self):
        return self.title

    def rating(self):
        l1st = [review.stars for review in self.reviews.all()]
        return (sum(l1st) / len(l1st)) if len(l1st) != 0 else "No reviews yet"


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=True, related_name='reviews')
    stars = models.FloatField(default=None, choices=((1, '★'),
                                                     (2, '★★'),
                                                     (3, '★★★'),
                                                     (4, '★★★★'),
                                                     (5, '★★★★★'),))

