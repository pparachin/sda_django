from django.db.models import (
    DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField,
    Model, TextField, ImageField
)
from django.contrib.auth.models import User


class Genre(Model):
    name = CharField(max_length=128)

    def __str__(self):
        return self.name


class Actor(Model):
    name = CharField(max_length=128)
    surname = CharField(max_length=128)
    birth_date = DateField(default=None)


class Movie(Model):
    title = CharField(max_length=128)
    genre = ForeignKey(Genre, on_delete=DO_NOTHING, default=None)
    rating = IntegerField(default=None)
    released = DateField(default=None)
    description = TextField(default=None)
    image = ImageField(upload_to='images/', default=None, null=True)
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Watchlist(Model):
    user = ForeignKey(User, on_delete=DO_NOTHING, default=None)
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, default=None)
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.movie.title


class Review(Model):
    user = ForeignKey(User, on_delete=DO_NOTHING, default=None)
    movie = ForeignKey(Movie, on_delete=DO_NOTHING, default=None)
    rating = IntegerField(default=None)
    text = TextField(default=None)
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.movie.title

