from django.urls import path
from . import views

app_name = 'helpmefind'

urlpatterns = [
    path('', views.find_doctor, name="find_doctor"),  # ✅ Directly link to your view
]
