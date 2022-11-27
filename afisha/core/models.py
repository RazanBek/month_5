from django.db import models


class Director(models.Model):
    name = models.CharField(default='Ваня', max_length=65)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(null=True, max_length=60)
    description = models.TextField(null=True)
    duration = models.IntegerField(null=True)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True, related_name='movies')

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(null=True)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=True, related_name='reviews')
