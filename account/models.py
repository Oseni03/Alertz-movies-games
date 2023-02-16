from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings

from alert.models import Movie, Games

# Create your models here.
class Customer(AbstractUser):

    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    movies = models.ManyToManyField(
        Movie, related_name="users", through="MovieAlert")
    games = models.ManyToManyField(
        Games, related_name="users", through="GameAlert")

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.username}"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            settings.EMAIL_USERNAME,
            [self.email],
            fail_silently=False,
        )

    @property
    def get_alert_count(self):
        return self.games.all().count() + self.movies.all().count()


class MovieAlert(models.Model):
    user = models.ForeignKey(
        Customer, related_name="movie_alerts", on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        Movie, related_name="alerts", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["user", "movie"]]
    
    def save(self, *args, **kwargs):
        if self.user.get_alert_count >= self.user.plan.alert_limit:
            return
        super().save(*args, **kwargs)


class GameAlert(models.Model):
    user = models.ForeignKey(
        Customer, related_name="game_alerts", on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Games, related_name="alerts", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["user", "game"]]
    
    def save(self, *args, **kwargs):
        if self.user.get_alert_count >= self.user.plan.alert_limit:
            return
        super().save(*args, **kwargs)