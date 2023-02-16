from django.urls import path

from . import views

app_name = "alert"

urlpatterns = [
    path("", views.index, name="index"),
    path("movies/", views.all_movies, name="movies"),
    path("movies/released/", views.released_movies, name="released -movies"),
    path("games/released/", views.released_games, name="released-games"),
    path("games/", views.all_games, name="games"),
    path("movies/<slug:slug>/", views.genre_movies, name="genre-movies"),
    path("games/<slug:slug>/", views.platform_games, name="platform-games"),
    path("add-game/<int:id>/", views.add_game_alert, name="add-game"),
    path("add-movie/<int:id>/", views.add_movie_alert, name="add-movie"),
    
    path("contact/", views.contact, name="contact"),
    # path("pricing/", views.pricing, name="pricing"),
    
    
    path('checkout/', views.CheckoutView.as_view(), name='checkout'), #add
    path('create_subscription/<pk>/', views.StripeIntentView.as_view(), name='create_subscription'),
    # path("profile/", views.profile, name="profile"), # add this
]