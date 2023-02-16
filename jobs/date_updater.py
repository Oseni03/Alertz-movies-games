import datetime
from threading import Thread 

from django.db.models import Q

from alert.models import Games, Date, PlatForm, Movie 

class Updater:
    def __init__(self):
        self.tdate = datetime.date.today()
        self.dates = Date.objects.prefetch_related("movies", "games").filter(
            Q(date__lt=self.tdate) |
            Q(date=self.tdate)
        )
    
    def alert_user(self, obj):
        dates = self.dates.filter(date==self.tdate)
        for movie in date.movies.all():
            pass
        
    
    def movies_updater(self):
        dates = self.dates.filter(has_movies=True)
        for date in dates:
            date.movies.all().update(is_released=True)
        return "Done"
    
    def games_updater(self):
        dates = self.dates.filter(has_games=True)
        for date in dates:
            date.games.all().update(is_released=True)
        return "Done"
    
    def main(self):
        # first = Thread.start(self.movies_updater())
        # second = Thread.start(self.games_updater())
        # Thread.join([first, second])
        self.movies_updater()
        self.games_updater()
        print("Update completed")