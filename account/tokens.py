from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

from six import text_type
import pyotp

class AccountPasswordResetTokenGenerator(PasswordResetTokenGenerator):
  def _make_hash_value(self, user, timestamp):
    return (
        text_type(user.pk), text_type(timestamp), 
        text_type(user.is_active)
      )
  
  def generate_otp(self):
    self.totp = pyotp.TOTP('base32secret3232')
    return self.totp.now()
  
  def verify(self, otp):
    return self.totp.verify(otp)
  
  
account_activation_token = AccountPasswordResetTokenGenerator()


def reCAPTCHAValdation(token):
  result = request.post(
    "https://www.google.com/recaptcha/api/siteverify",
    data = {
      "secret": settings.RECAPTCHA_SECRET_KEY,
      "response": token
    })
  return result.json()
