from django.contrib import admin
from django.urls import path
from .views import SearchByNameOrNumberView, SignInView, SignUpView, SpamView, ContactView

urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('signin', SignInView.as_view()),
    path('contact', ContactView.as_view()),
    path('search', SearchByNameOrNumberView.as_view()),
    path('spam', SpamView.as_view()),
]
