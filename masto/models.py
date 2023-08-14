from django.db import models

# Create your models here.

from django.db import models
from accounts.models import CustomUser as User

class MastodonAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    access_token = models.CharField(max_length=200)
