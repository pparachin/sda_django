import re

from django.core.exceptions import ValidationError
from django.forms import (
    CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea,
    TextInput, EmailInput, PasswordInput, ModelForm, DateInput, NumberInput
)

from viewer.models import Genre, Movie, Actor, Review, Watchlist
from django.contrib.auth.forms import UserCreationForm


class ActorForm(ModelForm):
    class Meta:
        model = Actor
        fields = "__all__"

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'surname': TextInput(attrs={'class': 'form-control'}),
            'birth_date': DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genre', 'released', 'image']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'released': DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

    def clean_description(self):
        # Každá věta bude začínat velkým písmenem
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre'].name == 'commedy' and result['rating'] > 5:
            self.add_error('genre', '')
            self.add_error('rating', '')
            raise ValidationError(
                "Commedies aren't so good to be rated over 5."
            )
        return result


class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = ['movie']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movie'].widget.attrs['class'] = 'form-control'


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = "__all__"


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]

        widgets = {
            'rating': NumberInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'class': 'form-control'})
        }


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'email', 'last_name']
        """
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control'})
        }
        """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'first_name', 'email', 'last_name', 'password1', 'password2']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
