from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    fullname = models.CharField(max_length=125)