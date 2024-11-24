"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from viewer.views import (hello, stranka, index, MovieCreateView,
                          MoviesView, CustomLoginView, ProfileView, RegisterView, MovieUpdateView,
                          ActorsView, ActorCreateView, GenreView, GenreCreateView, GenreUpdateView, WatchlistView,
                          WatchlistAddView, ReviewCreateView, MovieDetailView)
from viewer.models import Genre, Movie
from django.contrib.auth import views

admin.site.register(Genre)
admin.site.register(Movie)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stranka/<hodnota>', stranka),
    path('hello', hello, name='hello'),
    path('', index, name='index'),

    path('login', CustomLoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register", RegisterView.as_view(), name="register"),

    path("profile", ProfileView.as_view(), name="profile"),

    path("actors/index",ActorsView.as_view(), name="actors_view"),
    path("actors/create", ActorCreateView.as_view(), name="actors_add"),

    path("genres/index", GenreView.as_view(), name="genres_view"),
    path("genres/create", GenreCreateView.as_view(), name="genres_add"),
    path("genres/update/<pk>", GenreUpdateView.as_view(), name="genres_update"),

    path('movie_add', MovieCreateView.as_view(), name='movie_add'),
    path('movies', MoviesView.as_view(), name='movies'),
    path('movie/update/<pk>', MovieUpdateView.as_view(), name="movie_update"),
    path('movie/detail/', MovieDetailView.as_view(), name="movie_detail"),

    path('review/add/', ReviewCreateView.as_view(), name='review_add'),

    path('watchlist', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/add', WatchlistAddView.as_view(), name='watchlist_add'),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)