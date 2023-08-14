from django.contrib import admin

# Register your models here.

from .models import MastodonAccount

admin.site.register(MastodonAccount)

