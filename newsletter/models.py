from django.db import models
from django.core.mail import send_mail

import uuid

# Create your models here.
class Newsletter(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(max_length = 254, unique=True, error_messages={"email": "Email already subscribed!"})
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def email_user(self, subject, message):
        send_mail(
          subject, message, "Admin@email.com",
          [self.email], fail_silently=False,
        )