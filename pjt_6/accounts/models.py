# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser # 상속받을 AbstractUser import

# Create your models here.
class User(AbstractUser):
    pass