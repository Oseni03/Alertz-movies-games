from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Q
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.http import JsonResponse  # add this 


import json  #add this
import stripe


from .models import Date, Genre, Movie, Games, PlatForm
from .filters import MovieFilter, GameFilter

from jobs import loader

# Create your views here.
def index(request):
    # loader.load_regions()
    # loader.load_platforms()
    # loader.load_genres()
    # loader.load_movies()
    # loader.load_games()
    context = {
        "genres": Genre.objects.filter(is_movie=True),
        "platforms": PlatForm.objects.all(),
        "released_movies": Movie.objects.prefetch_related("date", "region").filter(is_released=True).order_by("-date")[:5],
        "released_games": Games.objects.prefetch_related("date").filter(is_released=True).order_by("-date")[:5],
        "released": True,
    }
    
    query = request.GET.get("query")
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) | 
            Q(casts__icontains=query))
        games = Games.objects.filter(title__icontains=query)
        
        context["movies"] = movies
        context["games"] = games 
        context["search"] = True 
    
    return render(request, "alert/index.html", context)


def all_movies(request):
    dates = Date.objects.prefetch_related(
        "movies__genres", 
        "movies__region").filter(
            has_movies=True, 
            movies__is_released=False).distinct()

    filtered = MovieFilter(request.GET, queryset=dates)

    paginator = Paginator(filtered.qs, 10)
    page_number = request.GET.get("page")
    dates = paginator.get_page(page_number)
    context = {
        "dates": dates,
        "form": filtered.form,
        "released": False
    }
    return render(request, "alert/movies.html", context)
    
    
def released_movies(request):
    dates = Date.objects.prefetch_related("movies__genres", "movies__region").filter(has_movies=True, movies__is_released=True).distinct().order_by("-date")

    filtered = MovieFilter(request.GET, queryset=dates)

    paginator = Paginator(filtered.qs, 10)
    page_number = request.GET.get("page")
    dates = paginator.get_page(page_number)
    context = {
        "dates": dates,
        "form": filtered.form,
        "released": True,
    }
    return render(request, "alert/movies.html", context)


def all_games(request):
    dates = Date.objects.prefetch_related("games__platforms").filter(has_games=True, games__is_released=False).distinct()

    filtered = GameFilter(request.GET, queryset=dates)

    paginator = Paginator(filtered.qs, 10)
    page_number = request.GET.get("page")
    dates = paginator.get_page(page_number)

    context = {
        "dates": dates,
        "form": filtered.form,
    }
    return render(request, "alert/games.html", context)
    
    
def released_games(request):
    dates = Date.objects.prefetch_related("games__platforms").filter(has_games=True, games__is_released=True).distinct().order_by("-date")

    filtered = GameFilter(request.GET, queryset=dates)

    paginator = Paginator(filtered.qs, 10)
    page_number = request.GET.get("page")
    dates = paginator.get_page(page_number)

    context = {
        "dates": dates,
        "form": filtered.form,
        "released": True,
    }
    return render(request, "alert/games.html", context)


@login_required
def add_movie_alert(request, id):
    movie = get_object_or_404(Movie, id=id)
    user = request.user
    if movie not in user.movies.all():
        user.movies.add(movie)
        user.save()
    elif movie in user.movies.all():
        user.movies.remove(movie)
        user.save()
    return redirect(request.META["HTTP_REFERER"])


@login_required
def add_game_alert(request, id):
    game = get_object_or_404(Games, id=id)
    user = request.user
    if game not in user.games.all():
        user.games.add(game)
        user.save()
    elif game in user.games.all():
        user.games.remove(game)
        user.save()
    return redirect(request.META["HTTP_REFERER"])


def genre_movies(request, slug):
    genre = get_object_or_404(Genre, slug=slug, is_movie=True)
    dates = (
        Date.objects.prefetch_related("movies__genres", "movies__region")
        .filter(has_movies=True)
        .filter(movies__in=genre.movies.all(), movies__genres__is_movie=True, movies__is_released=False).distinct()
    )

    filtered = MovieFilter(request.GET, queryset=dates)

    paginator = Paginator(filtered.qs, 10)
    page_number = request.GET.get("page")
    dates = paginator.get_page(page_number)
    context = {
        "dates": dates,
        "form": filtered.form,
        "genre": genre,
    }
    return render(request, "alert/genre_movies.html", context)


def platform_games(request, slug):
    platform = get_object_or_404(PlatForm, slug=slug)
    dates = Date.objects.prefetch_related("games__platforms").filter(
        has_games=True).filter(games__in=platform.games.distinct(), games__is_released=False
    )

    filtered = GameFilter(request.GET, queryset=dates)

    paginator = Paginator(filtered.qs, 10)
    page_number = request.GET.get("page")
    dates = paginator.get_page(page_number)
    context = {
        "dates": dates,
        "form": filtered.form,
        "platform": platform,
    }
    return render(request, "alert/platform_games.html", context)


def contact(request):
    if request.POST:
      name = request.POST.get("name")
      email = request.POST.get("email")
      subject = request.POST.get("subject")
      query = request.POST.get("query")
      message = render_to_string("tools/emails/contact_email.html", {
        "subject": subject,
        "query": query,
        "name": name,
      })
      try:
        send_mail(
          subject, message, email,
          [settings.EMAIL_HOST_USER], 
          fail_silently=False,
        )
        messages.success(request, 'Message sent successfully. We will get back to you soon.')
      except BadHeaderError:
        messages.info(request, 'Invalid header found.')
    return render(request, "alert/contact.html")


# @method_decorator(login_required, name='dispatch')
# class CheckoutView(TemplateView):
#     template_name = "alert/checkout.html"

#     def get_context_data(self, **kwargs):
#         products = Product.objects.all()
#         context = super(CheckoutView, self).get_context_data(**kwargs)
#         context.update({
#             "products": products,
#             "STRIPE_PUBLIC_KEY": settings.STRIPE_TEST_PUBLIC_KEY
#         })
#         return context


# @method_decorator(login_required, name='dispatch')
# class StripeIntentView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             data = json.loads(request.body)
#             print(data)
#             payment_method = data['payment_method']

#             payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
#             djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

#         # This creates a new Customer and attaches the PaymentMethod in one API call.
#             customer = stripe.Customer.create(
#                 payment_method=payment_method,
#                 email=request.user.email,
#                 invoice_settings={
#                     'default_payment_method': payment_method
#                 }
#               )

#             djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
#             request.user.customer = djstripe_customer
         

#           # At this point, associate the ID of the Customer object with your
#           # own internal representation of a customer, if you have one.
#           # print(customer)

#           # Subscribe the user to the subscription created
#             subscription = stripe.Subscription.create(
#                 customer=customer.id,
#                 items=[
#                     {
#                       "price": data["price_id"],
#                     },
#                 ],
#                 expand=["latest_invoice.payment_intent"]
#               )

#             djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

#             request.user.subscription = djstripe_subscription
#             request.user.customer = djstripe_customer
#             request.user.save()

          
#             # creating the intent
#             price = Price.objects.get(id=self.kwargs["pk"])
#             intent = stripe.PaymentIntent.create(
#                 amount=price.unit_amount,
#                 currency='usd',
#                 customer=customer['id'],
#                 description="Software development services",
#                 metadata={
#                     "price_id": price.id
#                 }
#             )
        
#             return JsonResponse({
#                 'clientSecret': intent['client_secret']
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)})