from django.urls import path

from . import views

app_name = "newsletter"

urlpatterns = [
  path("subscribe/", views.subscribe, name="subscribe"), 
  path("unsubscribe/<slug:uuid>/", views.unsubscribe, name="unsubscribe"), 
]