from django.urls import path
from .views import Home, LogoutAndBlacklistAccessTokenView


urlpatterns = [
    path('', Home.as_view()),
    path('api/token/logout/', LogoutAndBlacklistAccessTokenView.as_view(), name='logout'),
]