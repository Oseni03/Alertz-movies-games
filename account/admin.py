from django.contrib import admin
from .models import Customer, MovieAlert, GameAlert

# Register your models here.
admin.site.register(Customer)
admin.site.register(MovieAlert)
admin.site.register(GameAlert)