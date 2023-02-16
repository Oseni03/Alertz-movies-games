from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


# Create your models here.
class Movie(models.Model):
    class TypeChoice(models.TextChoices):
        MOVIE = "MOVIE", _("Movie")
        TV = "TV", _("Tv")
        TV_EPISODE = "TV_EPISODE", _("Tv Episode")

    title = models.CharField(max_length=255)
    image = models.URLField(null=True, blank=True)
    casts = models.CharField(max_length=255)
    region = models.ForeignKey(
        "Region", 
        related_name="movies", 
        on_delete=models.PROTECT,
        db_index=True,
        db_tablespace="movie_indexes"
    )
    type = models.CharField(max_length=250, choices=TypeChoice.choices)
    genres = models.ManyToManyField("Genre", related_name="movies", db_index=True, db_tablespace="movie_indexes")
    genres_list = models.CharField(max_length=150, null=True, blank=True)
    date = models.ForeignKey("Date", related_name="movies", on_delete=models.CASCADE, db_index=True, db_tablespace="movie_indexes")
    is_active = models.BooleanField(default=True, db_index=True, db_tablespace="movie_indexes")
    is_released = models.BooleanField(default=False, db_index=True, db_tablespace="movie_indexes")
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True, db_index=True, db_tablespace="movie_indexes")

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.date.has_movies = True
        self.date.save()
        super().save(*args, **kwargs)

    # @property
    # def get_genres(self):
    #     genres = self.genres.values_list("name")
    #     genres = [genre[0] for genre in genres]
    #     genres = str(genres).replace("[", "").replace("]", "").replace("'", "")
    #     return genres


class PlatForm(models.Model):
    name = models.CharField(max_length=35, unique=True, db_index=True, db_tablespace="platform_indexes")
    slug = models.SlugField(unique=True, null=True, blank=True, db_index=True, db_tablespace="platform_indexes")
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["name"]


class Games(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    platforms = models.ManyToManyField(PlatForm, related_name="games", db_index=True, db_tablespace="game_indexes")
    genres = models.ManyToManyField("Genre", related_name="games", db_index=True, db_tablespace="game_indexes")
    genres_list = models.CharField(max_length=150, null=True, blank=True)
    date = models.ForeignKey("Date", related_name="games", on_delete=models.CASCADE, db_index=True, db_tablespace="game_indexes")
    platform_list = models.CharField(max_length=150, null=True, blank=True)
    is_released = models.BooleanField(default=False, db_index=True, db_tablespace="game_indexes")
    is_active = models.BooleanField(default=True, db_index=True, db_tablespace="game_indexes")
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True, db_index=True, db_tablespace="game_indexes")

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.date.has_games = True
        self.date.save()
        super().save(*args, **kwargs)
    
    @property
    def get_platforms(self):
        platforms = self.platforms.values_list("name")
        platforms = [platform[0] for platform in platforms]
        platforms = str(platforms).replace("[", "").replace("]", "").replace("'", "").replace(", ", "/")
        return platforms 
    
    
    @property
    def get_genres(self):
        genres = self.genres.values_list("name")
        genres = [genre[0] for genre in genres]
        genres = str(genres).replace("[", "").replace("]", "").replace("'", "")
        return genres


class Region(models.Model):
    country = models.CharField(max_length=50, unique=True, db_index=True, db_tablespace="region_indexes")
    code = models.CharField(max_length=2, unique=True, db_index=True, db_tablespace="region_indexes")
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True, db_index=True, db_tablespace="region_indexes")

    def __str__(self):
        return str(self.country)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.country)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["country"]


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, db_tablespace="genre_indexes")
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True, db_index=True, db_tablespace="genre_indexes")
    is_game = models.BooleanField(default=False, db_index=True, db_tablespace="genre_indexes")
    is_movie = models.BooleanField(default=False, db_index=True, db_tablespace="genre_indexes")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ["name"]


class Date(models.Model):
    date = models.DateField(unique=True)
    has_games = models.BooleanField(default=False, db_index=True, db_tablespace="date_indexes")
    has_movies = models.BooleanField(default=False, db_index=True, db_tablespace="date_indexes")
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        ordering = ["date"]
