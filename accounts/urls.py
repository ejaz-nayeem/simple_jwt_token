# accounts/urls.py
from django.urls import path
from .views import RegisterView # Import the new view

urlpatterns = [
    # ... your other urls
    path('register/', RegisterView.as_view(), name='register'),
]