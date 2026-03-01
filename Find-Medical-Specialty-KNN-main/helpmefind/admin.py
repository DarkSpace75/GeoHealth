from django.contrib import admin

# Register your models here.
from .models import symptoms,cities

admin.site.register(symptoms)

admin.site.register(cities)
