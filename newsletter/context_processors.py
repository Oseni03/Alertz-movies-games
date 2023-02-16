from .forms import NewsletterForm

def newsletter(request):
    return {
        "newsletter_form": NewsletterForm(),
    }