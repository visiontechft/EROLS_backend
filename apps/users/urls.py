# ========== apps/users/urls.py ==========
from django.urls import path
from .views import RegisterView, ProfileView, login_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]