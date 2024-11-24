from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from viewer.forms import MovieForm, SignUpForm, ActorForm, GenreForm, WatchlistForm,ReviewForm
from django.views.generic import FormView, ListView, TemplateView, UpdateView
from viewer.models import Movie, Actor, Genre, Watchlist, Review


# from hollymovies.viewer.forms import SignUpForm


# Create your views here.
def hello(request):
    value = request.GET.get('value', '')
    aa = request.GET.get('parametr', '')
    if value == 10:
        print()
    return HttpResponse(f'Hello, {value} World! {aa}')


def stranka(request, hodnota):
    return HttpResponse(f'Hodnota stránky: {hodnota}')


def index(request):
    value = request.GET.get('value', '')
    return render(request, template_name='index.html', context={'hodnota': value})


"""
def movie_add(request):
    form = MovieForm()
    return render(request, template_name='movie_add.html', context={'form': form})
"""


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Nesprávně uživatelské jméno nebo heslo")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(TemplateView):
    template_name = 'profile.html'


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('movies')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description']
        )
        return result


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie


class GenreView(ListView):
    template_name = 'genres/index.html'
    model = Genre


class GenreCreateView(FormView):
    template_name = 'form.html'
    form_class = GenreForm
    success_url = reverse_lazy('genres_view')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Genre.objects.create(
            name=cleaned_data['name'],
        )
        return result


class GenreUpdateView(UpdateView):
    template_name = 'genres/edit_form.html'
    form_class = GenreForm
    model = Genre
    success_url = reverse_lazy('genres_view')


class MovieUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = MovieForm
    model = Movie
    success_url = reverse_lazy('movies')


class MovieDetailView(TemplateView):
    template_name = 'movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.request.GET.get('movie')
        context['movie'] = Movie.objects.get(pk=movie_id)
        context['reviews'] = Review.objects.filter(movie=movie_id)
        return context


class ActorsView(ListView):
    template_name = 'actors/index.html'
    model = Actor


class ActorCreateView(FormView):
    template_name = 'actors/create_form.html'
    form_class = ActorForm
    success_url = reverse_lazy('actors_view')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('actors/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Actor.objects.create(
            name=cleaned_data['name'],
            surname=cleaned_data['surname'],
            birth_date=cleaned_data['birth_date'],
        )
        print(result)
        return result


class WatchlistView(ListView):
    template_name = 'watchlist/index.html'
    model = Watchlist

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class WatchlistAddView(FormView):
    template_name = 'watchlist/add_movie_to_watchlist.html'
    form_class = WatchlistForm
    success_url = reverse_lazy('watchlist')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Watchlist.objects.create(
            user=self.request.user,
            movie=cleaned_data['movie']
        )
        return result


class ReviewCreateView(FormView):
    template_name = 'review_add_form.html'
    form_class = ReviewForm
    success_url = reverse_lazy('movies')

    # Get the movie id from the URL and then get the movie object and pass it to the form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.request.GET.get('movie')
        context['movie'] = Movie.objects.get(pk=movie_id)
        #context['informace'] = Genre.objects.get(pk=1)
        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        movie_id = self.request.GET.get('movie')
        movie = Movie.objects.get(pk=movie_id)
        Review.objects.create(
            user=self.request.user,
            movie=movie,
            rating=cleaned_data['rating'],
            text=cleaned_data['text']
        )
        return result