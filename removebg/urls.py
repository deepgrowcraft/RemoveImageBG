from django.urls import path
from . import views

urlpatterns = [
    path('removebg', views.remove_background, name='home'),  # Example URL pattern for the home view
]