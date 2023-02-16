import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include('account.urls', namespace="account")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path("newsletter/", include("newsletter.urls", namespace="newsletter")),
    path("__debug__", include(debug_toolbar.urls)),
    path('', include('alert.urls', namespace="alert")),
]