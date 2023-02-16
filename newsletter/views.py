from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import NewsletterForm
from .models import Newsletter 

# Create your views here.
@require_POST
def subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request, "newsletter/thanks.html")
    else:
        for error in form.errors.values():
            messages.info(request, error)
        return render(request, "newsletter/newsletter.html")


def unsubscribe(request, uuid):
  subscriber = get_object_or_404(Newsletter, uuid=uuid)
  subscriber.is_active = False 
  subscriber.save()
  return render(request, "newsletter/unsubscribe.html")