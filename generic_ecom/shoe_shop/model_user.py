from django.contrib.auth.models import AbstractUser
from django.db import models

# @python_2_unicode_compatible
class ExtendedUser(AbstractUser):
    mailing_address = models.TextField(default="", blank=True)
    billing_address = models.TextField(default="", blank=True)