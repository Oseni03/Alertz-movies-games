import django_filters
import datetime

from .models import Date, Genre, Games, Region, Movie, PlatForm


years = []
tyear = datetime.date.today().year 
for n in range(0, 3):
    year = tyear + n
    years.append((year, year))


def movie_genres(request):
    if request is not None:
        return Genre.objects.none()
    return Genre.objects.filter(is_movie=True)


def game_genres(request):
    if request is not None:
        return Genre.objects.none()
    return Genre.objects.filter(is_game=True)


def regions(request):
    if request is not None:
        return Region.objects.none()
    return Region.objects.all()


def platforms(request):
    if request is not None:
        return PlatForm.objects.none()
    return PlatForm.objects.all()


class MovieFilter(django_filters.FilterSet):
    movies__genres = django_filters.ModelChoiceFilter(queryset=movie_genres, empty_label="Genre")
    movies__type = django_filters.ChoiceFilter(choices=Movie.TypeChoice.choices, empty_label="Type")
    year = django_filters.ChoiceFilter(field_name='date', lookup_expr='year', choices=years, empty_label="Year")
    movies__region = django_filters.ModelChoiceFilter(queryset=regions, empty_label="Region")
    
    class Meta:
        model = Date
        fields = {
            "movies__genres": ["exact"],
            "movies__type": ["exact"],
            "movies__region": ["exact"],
        }


class GameFilter(django_filters.FilterSet):
    genre = django_filters.ModelChoiceFilter(field_name='games__genres', lookup_expr='exact', queryset=game_genres, empty_label="Genre")
    platform = django_filters.ModelChoiceFilter(field_name='games__platforms', lookup_expr='exact', queryset=platforms, empty_label="Platform")
    year = django_filters.ChoiceFilter(field_name='date', lookup_expr='year', choices=years, empty_label="Year")
    class Meta:
        model = Date 
        fields = ["date", "games"]