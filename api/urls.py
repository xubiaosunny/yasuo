from django.urls import path

from api.views.core import auth

urlpatterns = [
    path('auth/token/', auth.TokenView.as_view()),
]
